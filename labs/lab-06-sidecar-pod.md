# Lab 6 — Multi-Container Pods (Sidecar Pattern)

A Pod can hold more than one container that share the same network and (optionally) the same volumes. The CKAD exam tests three patterns: **sidecar**, **ambassador**, and **adapter**. This lab focuses on the sidecar — a helper container that augments the main app.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Sidecar that streams a shared log file

```bash
alias k=kubectl
cat > sidecar.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  volumes:
  - name: logs
    emptyDir: {}
  containers:
  - name: app
    image: busybox
    command: ["sh","-c","i=0; while true; do echo \"$(date) line $i\" >> /var/log/app.log; i=$((i+1)); sleep 2; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
  - name: log-shipper
    image: busybox
    command: ["sh","-c","tail -F /var/log/app.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
EOF
k apply -f sidecar.yaml
k get pod app-with-sidecar
```

The shared `emptyDir` volume is the glue: `app` writes, `log-shipper` reads.

---

## Step 2 — View each container's logs separately

```bash
k logs app-with-sidecar -c app | head
k logs app-with-sidecar -c log-shipper -f   # ctrl+C to stop
```

`-c <container>` selects the container when a Pod has more than one.

---

## Step 3 — Exec into a specific container

```bash
k exec -it app-with-sidecar -c app -- sh -c 'ls -l /var/log; head -3 /var/log/app.log'
```

---

## Step 4 — Ambassador pattern (preview)

The ambassador pattern fronts the main app with a proxy container (e.g. envoy or a tunneling sidecar). The structure is identical to Step 1 — two containers sharing the Pod's network namespace — only the helper does network proxying instead of log shipping.

---

## Step 5 — Clean up

```bash
k delete pod app-with-sidecar --force --grace-period 0
```

---

## What you learned
- Multiple containers share the Pod's network and selected volumes.
- `kubectl logs -c <container>` and `kubectl exec -c <container>` for multi-container Pods.
- The sidecar pattern: a helper that reads/writes a shared volume.
