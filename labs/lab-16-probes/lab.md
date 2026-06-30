# Lab 16 — Liveness, Readiness, and Startup Probes

Kubernetes uses three probes to manage container health: **livenessProbe** restarts a failed container, **readinessProbe** removes it from Service endpoints, **startupProbe** gives slow apps time to boot before liveness begins. CKAD 2026 tests all three probe types (`httpGet`, `tcpSocket`, `exec`) and their timing fields.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25`, `redis:7`, `busybox` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — HTTP liveness + readiness probe

```bash
cat > http-probes.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web-probes
  labels:
    app: web
spec:
  containers:
  - name: web
    image: nginx:1.25
    ports:
    - containerPort: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 2
      periodSeconds: 5
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 3
EOF
k apply -f http-probes.yaml
k get pod web-probes -w
```

Wait until `READY 1/1` then press Ctrl+C.

---

## Step 3 — Trigger a liveness failure

```bash
k exec web-probes -- rm /usr/share/nginx/html/index.html
sleep 35
k get pod web-probes
```

After `failureThreshold: 3` failed probes the container is restarted. Watch the `RESTARTS` counter increment.

---

## Step 4 — TCP socket probe

```bash
cat > tcp-probe.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: db-probe
spec:
  containers:
  - name: db
    image: redis:7
    ports:
    - containerPort: 6379
    readinessProbe:
      tcpSocket:
        port: 6379
      periodSeconds: 5
EOF
k apply -f tcp-probe.yaml
k get pod db-probe
```

A TCP probe succeeds when the TCP handshake completes — no HTTP server required.

---

## Step 5 — Exec probe + startupProbe for slow-starting apps

```bash
cat > slow-start.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: slow
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "sleep 20 && touch /tmp/ready && sleep 3600"]
    startupProbe:
      exec:
        command: ["cat", "/tmp/ready"]
      failureThreshold: 30
      periodSeconds: 5
    livenessProbe:
      exec:
        command: ["cat", "/tmp/ready"]
      periodSeconds: 10
EOF
k apply -f slow-start.yaml
k get pod slow -w
```

`startupProbe` runs exclusively until it succeeds. `failureThreshold: 30` × `periodSeconds: 5` = 150 seconds of startup budget before Kubernetes kills the container.

---

## Step 6 — Clean up

```bash
k delete pod web-probes db-probe slow --force --grace-period=0
```

---

## Free online tools

- **Probes docs**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- **Probe field reference**: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#ProbeHandler
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three probe types: `httpGet`, `tcpSocket`, `exec` — pick by what the container exposes.
- `initialDelaySeconds` + `periodSeconds` + `failureThreshold` control probe timing.
- `startupProbe` blocks liveness and readiness until the app is fully initialised.
- `readinessProbe` failure removes the Pod from Service endpoints without restarting it.
