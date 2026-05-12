# Lab 22 — Secrets

Secrets are like ConfigMaps but base64-encoded at rest and excluded from most listings by default. In this lab you will create generic and TLS secrets, inject them as env vars and files, and read them from inside a Pod.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create a generic Secret

```bash
alias k=kubectl
k create secret generic db-cred \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASS=s3cr3t
k get secret db-cred -o yaml
```

The values are base64 — **encoded**, not encrypted. Treat them as plaintext.

---

## Step 2 — Decode the value

```bash
k get secret db-cred -o jsonpath='{.data.DB_PASS}' | base64 -d; echo
```

---

## Step 3 — Inject Secret keys as env vars

```bash
cat > pod-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: client }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","echo user=$DB_USER pass=$DB_PASS; sleep 3600"]
    envFrom:
    - secretRef: { name: db-cred }
EOF
k apply -f pod-env.yaml
sleep 3
k logs client
```

---

## Step 4 — Mount a Secret as files

```bash
cat > pod-vol.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: vol }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","ls /etc/sec; cat /etc/sec/DB_PASS; sleep 3600"]
    volumeMounts:
    - { name: s, mountPath: /etc/sec, readOnly: true }
  volumes:
  - name: s
    secret: { secretName: db-cred, defaultMode: 0400 }
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
k exec vol -- ls -l /etc/sec
```

`defaultMode: 0400` means only the file owner can read the secret file — exam favourite.

---

## Step 5 — TLS Secret

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
k create secret tls demo-tls --cert=tls.crt --key=tls.key
k get secret demo-tls -o jsonpath='{.type}'; echo
```

The type field becomes `kubernetes.io/tls`.

---

## Step 6 — Image pull Secret (docker-registry)

```bash
k create secret docker-registry myreg \
  --docker-server=registry.example.com \
  --docker-username=u --docker-password=p --docker-email=u@example.com
k get secret myreg -o jsonpath='{.type}'; echo
```

Reference in a Pod with `spec.imagePullSecrets: [{ name: myreg }]`.

---

## Step 7 — Clean up

```bash
k delete pod client vol --force --grace-period 0
k delete secret db-cred demo-tls myreg
rm tls.crt tls.key
```

---

## What you learned
- Three Secret types: `generic`, `tls`, `docker-registry`.
- Inject via `envFrom: secretRef` or volume mount with `defaultMode`.
- Secrets are base64-encoded, not encrypted — protect them with RBAC.
