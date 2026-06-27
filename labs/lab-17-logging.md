# Lab 17 — Container Logging

`kubectl logs` is the first debugging tool on the CKAD exam. In this lab you will read logs from single and multi-container Pods, follow a live stream, retrieve logs from a crashed container, and aggregate logs across a Deployment.

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

## Step 2 — Create a noisy Pod and read its logs

```bash
k run noisy --image=busybox --restart=Never -- sh -c \
  'i=0; while true; do echo "line $i $(date)"; i=$((i+1)); sleep 1; done'
sleep 5
k logs noisy | tail -5
k logs noisy --tail=10
```

`--tail=N` limits output to the last N lines — useful when logs are very long.

---

## Step 3 — Follow logs in real time

```bash
k logs -f noisy &
sleep 6
kill %1
```

`-f` streams new log lines as they are written — equivalent to `tail -f`.

---

## Step 4 — Retrieve logs from a crashed container

```bash
k run crasher --image=busybox --restart=Always -- sh -c 'echo about to die; sleep 3; exit 1'
sleep 25
k get pod crasher
k logs crasher --previous | head -5
```

`--previous` retrieves logs from the prior terminated container. This is the primary tool for diagnosing crash loops — the current container may have no logs yet.

---

## Step 5 — Multi-container Pod logs

```bash
cat > multi.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: multi
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "while true; do echo APP $(date); sleep 1; done"]
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "while true; do echo SIDE $(date); sleep 1; done"]
EOF
k apply -f multi.yaml
sleep 5
k logs multi -c app | head -3
k logs multi -c sidecar | head -3
k logs multi --all-containers=true --prefix=true | head -8
```

`--prefix=true` adds `[pod/container]` labels to every line — essential when tailing multiple containers.

---

## Step 6 — Aggregate logs across a Deployment

```bash
k create deployment fleet --image=busybox --replicas=3 \
  -- sh -c 'while true; do echo $(hostname); sleep 1; done'
sleep 5
k logs deployment/fleet --tail=3
k logs -l app=fleet --prefix=true --tail=2
```

`-l <selector>` targets all Pods matching the label — no need to know individual Pod names.

---

## Step 7 — Clean up

```bash
k delete pod noisy crasher multi --force --grace-period=0
k delete deployment fleet
```

---

## Free online tools

- **kubectl logs reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/
- **Logging architecture**: https://kubernetes.io/docs/concepts/cluster-administration/logging/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl logs --tail=N` for recent lines; `-f` for live streaming.
- `--previous` is the key to diagnosing CrashLoopBackOff pods.
- `-c <container>` selects a specific container in a multi-container Pod.
- `-l <selector>` aggregates logs from all matching Pods simultaneously.
