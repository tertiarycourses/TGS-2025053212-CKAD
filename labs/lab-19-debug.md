# Lab 19 — Debugging Pods and Events

When a Pod won't run, the CKAD exam expects you to find the root cause fast. In this lab you will diagnose three failure modes (image pull error, CrashLoopBackOff, OOMKilled) using `describe`, `events`, `logs --previous`, and `kubectl debug`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — ImagePullBackOff

```bash
alias k=kubectl
k run typo --image=ngnix:1.25     # misspelled image
sleep 20
k get pod typo
k describe pod typo | tail -15
```

The bottom of `describe` shows Events with `Failed to pull image …`. Fix it:

```bash
k delete pod typo --force --grace-period 0
k run typo --image=nginx:1.25
```

---

## Step 2 — CrashLoopBackOff

```bash
k run crash --image=busybox --restart=Always -- sh -c 'echo starting; sleep 2; exit 1'
sleep 25
k get pod crash
k describe pod crash | grep -A2 "Last State"
k logs crash --previous
```

`--previous` shows what the crashed container printed before it died.

---

## Step 3 — OOMKilled

```bash
cat > oom.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: hungry }
spec:
  containers:
  - name: c
    image: polinux/stress
    command: ["stress"]
    args: ["--vm","1","--vm-bytes","200M","--vm-hang","1"]
    resources:
      limits: { memory: "64Mi" }
EOF
k apply -f oom.yaml
sleep 15
k describe pod hungry | grep -A3 "Last State"
```

Look for `Reason: OOMKilled`. Resolution: raise the memory limit or trim the workload.

---

## Step 4 — Cluster-wide event stream

```bash
k get events -A --sort-by=.lastTimestamp | tail -20
k get events --field-selector type=Warning
```

---

## Step 5 — `kubectl debug` ephemeral container

```bash
k debug crash -it --image=busybox --target=crash -- sh -c 'echo inside-debug; ls /proc/1; exit'
```

`kubectl debug` attaches an **ephemeral container** to a running Pod — handy when the main image lacks a shell.

---

## Step 6 — Clean up

```bash
k delete pod typo crash hungry --force --grace-period 0
```

---

## What you learned
- The three classic failure events: `ImagePullBackOff`, `CrashLoopBackOff`, `OOMKilled`.
- `kubectl describe`, `kubectl get events`, `kubectl logs --previous`.
- `kubectl debug` injects an ephemeral container for live triage.
