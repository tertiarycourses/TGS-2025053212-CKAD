# Lab 30 — NetworkPolicy

By default every Pod can talk to every other Pod. NetworkPolicies tighten that by allow-listing traffic. In this lab you will deny everything in a namespace, then carefully allow client → backend traffic.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

> Killercoda's default Kubernetes playground enforces NetworkPolicy via the cluster's CNI. If your scenario uses a CNI that does not enforce policies, install Calico first: `kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml`.

---

## Step 1 — Baseline workloads

```bash
alias k=kubectl
k create ns secured
k -n secured create deployment backend --image=hashicorp/http-echo -- -text=backend-ok
k -n secured expose deployment backend --port=5678
k -n secured run client-ok  --image=busybox --labels=role=allowed --command -- sh -c 'sleep 3600'
k -n secured run client-bad --image=busybox --labels=role=blocked --command -- sh -c 'sleep 3600'
k -n secured wait --for=condition=Ready pod --all --timeout=60s
```

Confirm both clients can reach the backend (no policy yet):

```bash
for p in client-ok client-bad; do
  echo "--- $p ---"
  k -n secured exec $p -- wget -qO- --timeout=3 backend:5678
done
```

---

## Step 2 — Default deny (all ingress)

```bash
cat > deny.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: secured
spec:
  podSelector: {}
  policyTypes: [ Ingress ]
EOF
k apply -f deny.yaml
```

Re-test — both clients now time out:

```bash
k -n secured exec client-ok -- wget -qO- --timeout=3 backend:5678 || echo "blocked"
```

---

## Step 3 — Allow only `role=allowed` → backend

```bash
cat > allow.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-allowed
  namespace: secured
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes: [ Ingress ]
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

Re-test:

```bash
k -n secured exec client-ok  -- wget -qO- --timeout=3 backend:5678
k -n secured exec client-bad -- wget -qO- --timeout=3 backend:5678 || echo "still blocked"
```

`client-ok` works, `client-bad` is still blocked.

---

## Step 4 — Egress lockdown (DNS only)

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
  policyTypes: [ Egress ]
  egress:
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - { protocol: UDP, port: 53 }
    - { protocol: TCP, port: 53 }
EOF
k apply -f egress.yaml
k -n secured exec client-bad -- wget -qO- --timeout=3 http://example.com || echo "egress blocked"
```

---

## Step 5 — Clean up

```bash
k delete ns secured
```

---

## What you learned
- Default-deny pattern: empty `podSelector: {}` + `policyTypes: [Ingress]`.
- Allow rules combine `podSelector` and/or `namespaceSelector` with port lists.
- Egress works the same way — common pattern is "deny all egress except DNS".
