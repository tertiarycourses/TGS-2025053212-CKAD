# Lab 22 — Secrets

Secrets are like ConfigMaps but base64-encoded and with stricter access controls. CKAD 2026 tests `generic`, `tls`, and `docker-registry` Secret types, env-var injection, file-volume mounting with `defaultMode`, and decoding values. Secrets are not encrypted by default — protect them with RBAC.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `openssl` (pre-installed on Killercoda)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create a generic Secret

```bash
k create secret generic db-cred \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASS=s3cr3t
k get secret db-cred -o yaml
```

Values are base64-encoded (not encrypted). Anyone with `get secret` RBAC can decode them.

---

## Step 3 — Decode a Secret value

```bash
k get secret db-cred -o jsonpath='{.data.DB_PASS}' | base64 -d; echo
```

Expected: `s3cr3t`

---

## Step 4 — Inject Secret keys as environment variables

```bash
cat > pod-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: client
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "echo user=$DB_USER pass=$DB_PASS; sleep 3600"]
    envFrom:
    - secretRef:
        name: db-cred
EOF
k apply -f pod-env.yaml
sleep 3
k logs client
```

---

## Step 5 — Mount a Secret as files with restrictive permissions

```bash
cat > pod-vol.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: vol
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "ls -l /etc/sec; cat /etc/sec/DB_PASS; sleep 3600"]
    volumeMounts:
    - name: s
      mountPath: /etc/sec
      readOnly: true
  volumes:
  - name: s
    secret:
      secretName: db-cred
      defaultMode: 0400
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
k exec vol -- ls -l /etc/sec
```

`defaultMode: 0400` — owner read-only. CKAD frequently asks you to set this.

---

## Step 6 — TLS Secret

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
k create secret tls demo-tls --cert=tls.crt --key=tls.key
k get secret demo-tls -o jsonpath='{.type}'; echo
```

Type is `kubernetes.io/tls`. Used with Ingress TLS termination (Lab 29).

---

## Step 7 — Docker registry Secret

```bash
k create secret docker-registry myreg \
  --docker-server=registry.example.com \
  --docker-username=myuser \
  --docker-password=mypass \
  --docker-email=myuser@example.com
k get secret myreg -o jsonpath='{.type}'; echo
```

Reference in a Pod: `spec.imagePullSecrets: [{name: myreg}]`.

---

## Step 8 — Clean up

```bash
k delete pod client vol --force --grace-period=0
k delete secret db-cred demo-tls myreg
rm -f tls.crt tls.key
```

---

## Free online tools

- **Secrets docs**: https://kubernetes.io/docs/concepts/configuration/secret/
- **Secret types reference**: https://kubernetes.io/docs/concepts/configuration/secret/#secret-types
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three Secret types: `generic`, `tls` (`kubernetes.io/tls`), `docker-registry`.
- `envFrom: secretRef` injects all keys; `env.valueFrom.secretKeyRef` injects one key.
- Volume mount with `defaultMode: 0400` is exam-tested — restricts file to owner read-only.
- Secrets are base64-encoded, not encrypted — use RBAC to restrict access.
