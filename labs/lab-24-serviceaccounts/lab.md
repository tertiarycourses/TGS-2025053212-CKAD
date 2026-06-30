# Lab 24 — ServiceAccounts

Every Pod runs as a ServiceAccount. The `default` ServiceAccount has minimal RBAC permissions. CKAD 2026 tests creating dedicated ServiceAccounts, attaching them to Pods, disabling the auto-mounted token, and requesting short-lived tokens with `kubectl create token`.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `bitnami/kubectl:latest` image (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create a ServiceAccount

```bash
k create serviceaccount app-sa
k get sa
k describe sa app-sa
```

---

## Step 3 — Attach the ServiceAccount to a Pod

```bash
cat > pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  serviceAccountName: app-sa
  containers:
  - name: c
    image: bitnami/kubectl:latest
    command: ["sh", "-c", "sleep 3600"]
EOF
k apply -f pod.yaml
k get pod app -o jsonpath='{.spec.serviceAccountName}'; echo
```

---

## Step 4 — Inspect the auto-mounted token inside the Pod

```bash
k exec app -- ls /var/run/secrets/kubernetes.io/serviceaccount/
k exec app -- sh -c 'cat /var/run/secrets/kubernetes.io/serviceaccount/namespace; echo'
```

Three files are projected: `token`, `ca.crt`, and `namespace`. The token is a short-lived JWT rotated automatically by the kubelet.

---

## Step 5 — Use the token to call the Kubernetes API

```bash
k exec app -- sh -c '
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CA=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
curl --cacert $CA -H "Authorization: Bearer $TOKEN" \
  https://kubernetes.default.svc/api/v1/namespaces/default/pods 2>/dev/null | grep -c "kind"'
```

You should see a 403 Forbidden — `app-sa` has no RBAC permissions yet. Lab 25 grants access.

---

## Step 6 — Disable token auto-mount (least privilege)

```bash
k patch sa app-sa -p '{"automountServiceAccountToken": false}'
```

Set this on Pods or ServiceAccounts that do not need API access. It removes the projected volume from the Pod.

---

## Step 7 — Request a short-lived ad-hoc token

```bash
TOKEN=$(k create token app-sa --duration=1h)
echo $TOKEN | cut -c1-60
echo "... (truncated)"
```

`kubectl create token` replaces the old long-lived Secret-backed tokens removed in Kubernetes 1.24+.

---

## Step 8 — Clean up

```bash
k delete pod app --force --grace-period=0
k delete sa app-sa
```

---

## Free online tools

- **ServiceAccount docs**: https://kubernetes.io/docs/concepts/security/service-accounts/
- **Configure ServiceAccounts**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Every Pod runs as a ServiceAccount (`default` if not specified).
- `spec.serviceAccountName` attaches a custom ServiceAccount to a Pod.
- Token, CA cert, and namespace are projected into `/var/run/secrets/kubernetes.io/serviceaccount/`.
- `automountServiceAccountToken: false` enforces least privilege for Pods that don't need API access.
- `kubectl create token <sa>` generates short-lived tokens — the modern replacement for Secret tokens.
