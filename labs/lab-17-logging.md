# Lab 17 — Container Logging

`kubectl logs` is the first tool you reach for on the CKAD exam. In this lab you will read logs from a single Pod, a multi-container Pod, follow logs in real time, and grep across many Pods.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — A noisy Pod

```bash
alias k=kubectl
k run noisy --image=busybox --restart=Never -- sh -c '
i=0; while true; do echo line $i $(date); i=$((i+1)); sleep 1; done'
sleep 5
k logs noisy | tail
```

---

## Step 2 — Follow in real time

```bash
k logs -f noisy &
sleep 6
kill %1
```

`-f` is the equivalent of `tail -f`.

---

## Step 3 — Previous container's logs (after a crash)

```bash
k run crasher --image=busybox --restart=Always -- sh -c 'echo about to die; sleep 3; exit 1'
sleep 20
k get pod crasher        # RESTARTS > 0
k logs crasher --previous | head
```

`--previous` retrieves logs from the prior terminated container, vital for debugging crash loops.

---

## Step 4 — Multi-container Pod logs

```bash
cat > multi.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: multi }
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh","-c","while true; do echo APP $(date); sleep 1; done"]
  - name: sidecar
    image: busybox
    command: ["sh","-c","while true; do echo SIDE $(date); sleep 1; done"]
EOF
k apply -f multi.yaml
sleep 5
k logs multi -c app | head -3
k logs multi -c sidecar | head -3
k logs multi --all-containers=true --prefix=true | head
```

`--prefix=true` adds `[pod/container]` labels to every line.

---

## Step 5 — Logs across many Pods with a selector

```bash
k create deployment fleet --image=busybox --replicas=3 -- sh -c 'while true; do echo $(hostname); sleep 1; done'
sleep 5
k logs deployment/fleet --tail=3
k logs -l app=fleet --prefix=true --tail=2
```

---

## Step 6 — Clean up

```bash
k delete pod noisy crasher multi --force --grace-period 0
k delete deployment fleet
```

---

## What you learned
- `kubectl logs`, `-f`, `--previous`, `--tail=N`.
- `-c <container>` and `--all-containers=true`.
- `-l <label>` to grep across many Pods.
