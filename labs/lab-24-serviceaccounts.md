# Lab 24 — ServiceAccounts

Every Pod runs as a ServiceAccount. The default ServiceAccount (`default`) has very little RBAC. In this lab you will create a dedicated ServiceAccount, attach it to a Pod, and request a short-lived API token.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create a ServiceAccount

```bash
alias k=kubectl
k create serviceaccount app-sa
k get sa
```

---

## Step 2 — Pod using the new ServiceAccount

```bash
cat > pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: app }
spec:
  serviceAccountName: app-sa
  containers:
  - name: c
    image: bitnami/kubectl:latest
    command: ["sh","-c","sleep 3600"]
EOF
k apply -f pod.yaml
k get pod app -o jsonpath='{.spec.serviceAccountName}'; echo
```

---

## Step 3 — Inspect the auto-mounted token inside the Pod

```bash
k exec app -- ls /var/run/secrets/kubernetes.io/serviceaccount/
k exec app -- sh -c 'cat /var/run/secrets/kubernetes.io/serviceaccount/namespace; echo'
```

The kubelet projects a short-lived token, `ca.crt`, and `namespace` into every Pod.

---

## Step 4 — Use the token to call the API

```bash
k exec app -- sh -c '
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CA=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
curl --cacert $CA -H "Authorization: Bearer $TOKEN" \
  https://kubernetes.default.svc/api/v1/namespaces/default/pods 2>/dev/null | head -3'
```

You should get a 403 — `app-sa` has no RBAC yet. Lab 25 fixes this.

---

## Step 5 — Disable token automount

```bash
k patch sa app-sa -p '{"automountServiceAccountToken": false}'
```

Set this on Pods (or the ServiceAccount) that don't need API access. It removes the projected volume and reduces blast radius.

---

## Step 6 — Request an ad-hoc token (`kubectl create token`)

```bash
TOKEN=$(k create token app-sa --duration=1h)
echo $TOKEN | cut -c1-60; echo "..."
```

`kubectl create token` returns a short-lived bearer token — the modern replacement for long-lived Secret-backed tokens.

---

## Step 7 — Clean up

```bash
k delete pod app --force --grace-period 0
k delete sa app-sa
```

---

## What you learned
- Pods always run as **a** ServiceAccount.
- Auto-mounted tokens live at `/var/run/secrets/kubernetes.io/serviceaccount/`.
- `automountServiceAccountToken: false` and `kubectl create token` for least privilege.
