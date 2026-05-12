# Lab 16 — Liveness, Readiness and Startup Probes

Kubernetes uses three probes to manage Pod lifecycle:

- **livenessProbe** — restart the container if it fails
- **readinessProbe** — remove the Pod from Service endpoints if it fails
- **startupProbe** — give slow-starting apps time before liveness kicks in

In this lab you will configure all three using HTTP, TCP and exec probe types.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Pod with HTTP liveness + readiness

```bash
alias k=kubectl
cat > http-probes.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: web-probes, labels: { app: web } }
spec:
  containers:
  - name: web
    image: nginx:1.25
    ports: [{ containerPort: 80 }]
    readinessProbe:
      httpGet: { path: /, port: 80 }
      initialDelaySeconds: 2
      periodSeconds: 5
    livenessProbe:
      httpGet: { path: /, port: 80 }
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 3
EOF
k apply -f http-probes.yaml
k get pod web-probes -w        # wait until READY 1/1, ctrl+C
```

---

## Step 2 — Simulate a liveness failure

```bash
k exec web-probes -- rm -f /usr/share/nginx/html/index.html
k exec web-probes -- sh -c 'echo broken > /etc/nginx/conf.d/default.conf'
k exec web-probes -- nginx -s reload || true
k get pod web-probes -w   # RESTARTS counter will increment, ctrl+C
```

---

## Step 3 — TCP probe

```bash
cat > tcp-probe.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: db-probe }
spec:
  containers:
  - name: db
    image: redis:7
    ports: [{ containerPort: 6379 }]
    readinessProbe:
      tcpSocket: { port: 6379 }
      periodSeconds: 5
EOF
k apply -f tcp-probe.yaml
k get pod db-probe
```

A TCP probe succeeds if the TCP handshake completes.

---

## Step 4 — Exec probe + startupProbe

```bash
cat > slow-start.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: slow }
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh","-c","sleep 30 && touch /tmp/ready && sleep 3600"]
    startupProbe:
      exec: { command: ["cat","/tmp/ready"] }
      failureThreshold: 30      # 30 × 5s = 150s max startup
      periodSeconds: 5
    livenessProbe:
      exec: { command: ["cat","/tmp/ready"] }
      periodSeconds: 10
EOF
k apply -f slow-start.yaml
k get pod slow -w     # READY 1/1 after ~30s, ctrl+C
```

`startupProbe` runs first; once it succeeds liveness takes over.

---

## Step 5 — Clean up

```bash
k delete pod web-probes db-probe slow --force --grace-period 0
```

---

## What you learned
- Three probe types (`httpGet`, `tcpSocket`, `exec`).
- `initialDelaySeconds`, `periodSeconds`, `failureThreshold`.
- `startupProbe` defers liveness for slow boots.
