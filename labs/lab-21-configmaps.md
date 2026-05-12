# Lab 21 — ConfigMaps (env and volume)

ConfigMaps inject **non-secret** configuration into Pods. CKAD tests three injection styles: individual env vars (`valueFrom.configMapKeyRef`), bulk env vars (`envFrom`), and file mounts. In this lab you will exercise all three.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create ConfigMaps three ways

```bash
alias k=kubectl
# from literals
k create configmap app-cfg --from-literal=COLOR=blue --from-literal=GREETING=hello

# from a file
cat > app.conf <<'EOF'
debug=true
log_level=info
EOF
k create configmap app-conf --from-file=app.conf

# from an env-file
cat > env.list <<'EOF'
TIMEOUT=30
RETRIES=5
EOF
k create configmap app-env --from-env-file=env.list

k get cm
```

---

## Step 2 — Inject a single key as an env var

```bash
cat > pod-single.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: single }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","echo COLOR=$COLOR; sleep 3600"]
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

---

## Step 3 — Inject all keys with `envFrom`

```bash
cat > pod-bulk.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: bulk }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","env | sort | grep -E 'COLOR|GREETING|TIMEOUT|RETRIES'; sleep 3600"]
    envFrom:
    - configMapRef: { name: app-cfg }
    - configMapRef: { name: app-env }
EOF
k apply -f pod-bulk.yaml
sleep 3
k logs bulk
```

---

## Step 4 — Mount a ConfigMap as a file

```bash
cat > pod-vol.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: vol }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","ls /etc/app; cat /etc/app/app.conf; sleep 3600"]
    volumeMounts:
    - { name: cfg, mountPath: /etc/app }
  volumes:
  - name: cfg
    configMap: { name: app-conf }
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
```

Each key in the ConfigMap becomes a file in the mounted directory.

---

## Step 5 — Live update — file mount picks up changes, env vars do not

```bash
k create configmap app-conf --from-file=app.conf=<(echo "debug=false") --dry-run=client -o yaml | k apply -f -
sleep 60
k exec vol -- cat /etc/app/app.conf
```

Mounted ConfigMap files are refreshed (typically within ~60 s). Env-var-injected values are **only** set at Pod startup — to refresh them you must restart the Pod.

---

## Step 6 — Clean up

```bash
k delete pod single bulk vol --force --grace-period 0
k delete cm app-cfg app-conf app-env
```

---

## What you learned
- Three ways to create ConfigMaps: `--from-literal`, `--from-file`, `--from-env-file`.
- Three ways to consume them: `configMapKeyRef`, `envFrom`, volume mount.
- File-mounted ConfigMaps update live; env-var injections do not.
