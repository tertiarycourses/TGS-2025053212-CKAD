# Lab 30 — NetworkPolicy

By default every Pod can communicate with every other Pod. NetworkPolicies restrict that traffic by allow-listing specific sources and destinations. CKAD 2026 regularly includes a NetworkPolicy question — you must write a default-deny policy and a selective allow policy from scratch.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

> Killercoda's Kubernetes playground enforces NetworkPolicy via the cluster CNI. If policies have no effect, install Calico:
> `kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml`

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `hashicorp/http-echo`, `busybox` images (pulled automatically)

---

## Step 1 — Set exam aliases and create workloads

```bash
alias k=kubectl
k create ns secured
k -n secured create deployment backend --image=hashicorp/http-echo -- -text=backend-ok
k -n secured expose deployment backend --port=5678
k -n secured run client-ok  --image=busybox --labels=role=allowed \
  --command -- sh -c 'sleep 3600'
k -n secured run client-bad --image=busybox --labels=role=blocked \
  --command -- sh -c 'sleep 3600'
k -n secured wait --for=condition=Ready pod --all --timeout=60s
```

Confirm both clients can reach the backend before any policy is applied:

```bash
for p in client-ok client-bad; do
  echo "--- $p ---"
  k -n secured exec $p -- wget -qO- --timeout=3 backend:5678
done
```

---

## Step 2 — Default deny: block all ingress

```bash
cat > deny.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: secured
spec:
  podSelector: {}
  policyTypes:
  - Ingress
EOF
k apply -f deny.yaml
```

`podSelector: {}` matches **all** Pods in the namespace. An empty `ingress:` list means no traffic is allowed in.

```bash
k -n secured exec client-ok -- wget -qO- --timeout=3 backend:5678 || echo "blocked"
```

---

## Step 3 — Selective allow: only role=allowed can reach the backend

```bash
cat > allow.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-role-allowed
  namespace: secured
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: allowed
    ports:
    - protocol: TCP
      port: 5678
EOF
k apply -f allow.yaml
```

```bash
k -n secured exec client-ok  -- wget -qO- --timeout=3 backend:5678
k -n secured exec client-bad -- wget -qO- --timeout=3 backend:5678 || echo "still blocked"
```

`client-ok` succeeds; `client-bad` is still blocked.

---

## Step 4 — Egress lockdown: allow DNS only

```bash
cat > egress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: egress-dns-only
  namespace: secured
spec:
  podSelector:
    matchLabels:
      role: blocked
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
EOF
k apply -f egress.yaml
k -n secured exec client-bad -- wget -qO- --timeout=3 http://example.com || echo "egress blocked"
```

The `client-bad` Pod can still resolve DNS but cannot make outbound TCP connections.

---

## Step 5 — Cross-namespace allow (namespaceSelector)

```bash
k create ns trusted
k label ns trusted purpose=trusted

cat > ns-allow.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-trusted-ns
  namespace: secured
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          purpose: trusted
EOF
k apply -f ns-allow.yaml
```

`namespaceSelector` allows all Pods from namespaces matching the label.

---

## Step 6 — Clean up

```bash
k delete ns secured trusted
```

---

## Free online tools

- **NetworkPolicy docs**: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- **NetworkPolicy editor** (visual): https://editor.networkpolicy.io
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Default-deny pattern: `podSelector: {}` + `policyTypes: [Ingress]` with no `ingress:` list.
- `podSelector` in `ingress.from` matches Pods by label within the same namespace.
- `namespaceSelector` in `ingress.from` matches all Pods in matching namespaces.
- Egress works the same way — the common exam pattern is "deny all egress except DNS (port 53)".
- NetworkPolicies are additive: multiple policies combine with logical OR on the allow rules.
