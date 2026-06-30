# Lab 21 — ConfigMaps (Environment and Volume Injection)

ConfigMaps inject non-secret configuration into Pods. CKAD 2026 tests all three injection styles: individual env vars (`valueFrom.configMapKeyRef`), bulk env vars (`envFrom`), and file-based volume mounts. You must also know that only file mounts update live — env vars require a Pod restart.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create ConfigMaps three ways

```bash
k create configmap app-cfg \
  --from-literal=COLOR=blue \
  --from-literal=GREETING=hello

cat > app.conf <<'EOF'
debug=true
log_level=info
EOF
k create configmap app-conf --from-file=app.conf

cat > env.list <<'EOF'
TIMEOUT=30
RETRIES=5
EOF
k create configmap app-env --from-env-file=env.list

k get cm
```

Three creation methods: `--from-literal` (key=value pairs), `--from-file` (file becomes a key), `--from-env-file` (dotenv format).

---

## Step 3 — Inject a single key as an environment variable

```bash
cat > pod-single.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: single
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "echo COLOR=$COLOR; sleep 3600"]
    env:
    - name: COLOR
      valueFrom:
        configMapKeyRef:
          name: app-cfg
          key: COLOR
EOF
k apply -f pod-single.yaml
sleep 3
k logs single
```

Expected: `COLOR=blue`

---

## Step 4 — Inject all keys with envFrom

```bash
cat > pod-bulk.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: bulk
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "env | grep -E 'COLOR|GREETING|TIMEOUT|RETRIES'; sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-cfg
    - configMapRef:
        name: app-env
EOF
k apply -f pod-bulk.yaml
sleep 3
k logs bulk
```

`envFrom` loads every key in the ConfigMap as an environment variable — no need to name them individually.

---

## Step 5 — Mount a ConfigMap as a file volume

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
    command: ["sh", "-c", "cat /etc/app/app.conf; sleep 3600"]
    volumeMounts:
    - name: cfg
      mountPath: /etc/app
  volumes:
  - name: cfg
    configMap:
      name: app-conf
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
```

Each key in the ConfigMap becomes a file in the mounted directory.

---

## Step 6 — Live update (file mount vs env var)

```bash
k create configmap app-conf \
  --from-file=app.conf=<(echo "debug=false") \
  --dry-run=client -o yaml | k apply -f -
sleep 60
k exec vol -- cat /etc/app/app.conf
```

The file mount updates automatically within ~60 seconds. Environment variable injections are **fixed at Pod startup** — to refresh them you must delete and recreate the Pod.

---

## Step 7 — Clean up

```bash
k delete pod single bulk vol --force --grace-period=0
k delete cm app-cfg app-conf app-env
```

---

## Free online tools

- **ConfigMaps docs**: https://kubernetes.io/docs/concepts/configuration/configmap/
- **Configure Pods with ConfigMaps**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three ConfigMap creation methods: `--from-literal`, `--from-file`, `--from-env-file`.
- Three consumption methods: `configMapKeyRef` (single key), `envFrom` (all keys), volume mount (file).
- Volume-mounted ConfigMaps update live; env-var injections require a Pod restart.
- `configMapRef` in `envFrom` vs `configMapKeyRef` in `env.valueFrom` — know both spellings.
