# Lab 19 — Debugging Pods and Events

CKAD 2026 regularly includes broken workloads that you must diagnose and fix within a time limit. In this lab you will identify and resolve three classic failure modes — `ImagePullBackOff`, `CrashLoopBackOff`, `OOMKilled` — and use `kubectl debug` for live triage.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25`, `busybox`, `polinux/stress` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Diagnose: ImagePullBackOff

```bash
k run typo --image=ngnix:1.25
sleep 20
k get pod typo
k describe pod typo | tail -15
```

Look for `Failed to pull image` in the Events section. The fix: delete and recreate with the correct image name.

```bash
k delete pod typo --force --grace-period=0
k run typo --image=nginx:1.25
```

---

## Step 3 — Diagnose: CrashLoopBackOff

```bash
k run crash --image=busybox --restart=Always -- sh -c 'echo starting; sleep 2; exit 1'
sleep 30
k get pod crash
k describe pod crash | grep -A3 "Last State"
k logs crash --previous
```

`--previous` shows what the crashed container printed before exiting. Fix the exit code in the command — in the exam, fix the container command or image per the question.

---

## Step 4 — Diagnose: OOMKilled

```bash
cat > oom.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: hungry
spec:
  containers:
  - name: c
    image: polinux/stress
    command: ["stress"]
    args: ["--vm", "1", "--vm-bytes", "200M", "--vm-hang", "1"]
    resources:
      limits:
        memory: "64Mi"
EOF
k apply -f oom.yaml
sleep 15
k describe pod hungry | grep -A4 "Last State"
```

Look for `Reason: OOMKilled`. Resolution: increase the `memory` limit or reduce the workload's footprint.

---

## Step 5 — Cluster-wide event stream

```bash
k get events -A --sort-by=.lastTimestamp | tail -20
k get events --field-selector type=Warning
```

`get events` is the fastest way to see what the cluster has been doing — more concise than `describe` across many Pods.

---

## Step 6 — kubectl debug: ephemeral container

```bash
k debug crash -it --image=busybox --target=crash -- sh -c 'ls /proc/1; echo inside-debug'
```

`kubectl debug` injects an **ephemeral container** into a running Pod — useful when the main container has no shell (distroless images). The ephemeral container shares the process namespace with the target.

---

## Step 7 — Clean up

```bash
k delete pod typo crash hungry --force --grace-period=0 --ignore-not-found
```

---

## Free online tools

- **Debugging Pods docs**: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
- **kubectl debug reference**: https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ImagePullBackOff` → wrong image name or tag; fix with `kubectl delete` + `kubectl run`.
- `CrashLoopBackOff` → container exits non-zero; use `kubectl logs --previous`.
- `OOMKilled` → container exceeded memory limit; raise `resources.limits.memory`.
- `kubectl get events --sort-by=.lastTimestamp` is faster than `describe` for cluster-wide diagnosis.
- `kubectl debug` injects an ephemeral shell into any running Pod.
