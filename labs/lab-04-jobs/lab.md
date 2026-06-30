# Lab 4 — Jobs (Run-to-Completion Workloads)

A Job runs Pods until a required number of successful completions is reached — then it stops. CKAD 2026 tests `completions`, `parallelism`, `backoffLimit`, and `activeDeadlineSeconds` in almost every sitting. You must be able to write a Job manifest from memory.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox`, `perl:5.34` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
```

---

## Step 2 — One-shot Job (imperative)

```bash
k create job hello --image=busybox -- echo "hello CKAD 2026"
k get jobs,pods -l job-name=hello
k logs -l job-name=hello
```

A Job creates a Pod, waits for it to exit 0, and marks the Job `Complete`. The Pod is retained for log inspection.

---

## Step 3 — Parallel Job with multiple completions

```bash
cat > parallel.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-parallel
spec:
  completions: 5
  parallelism: 2
  backoffLimit: 4
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: pi
        image: perl:5.34
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(50)"]
EOF
k apply -f parallel.yaml
k get job pi-parallel -w
```

Field definitions (memorise these for the exam):
- `completions: 5` — need five successful Pod completions
- `parallelism: 2` — run at most two Pods simultaneously
- `backoffLimit: 4` — allow up to four Pod failures before failing the Job
- `restartPolicy: Never` — required for Job Pod templates (not `Always`)

---

## Step 4 — Failing Job and backoffLimit

```bash
cat > fail.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: must-fail
spec:
  backoffLimit: 2
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: f
        image: busybox
        command: ["sh", "-c", "exit 1"]
EOF
k apply -f fail.yaml
sleep 30
k get pods -l job-name=must-fail
k describe job must-fail | grep -A2 Conditions
```

After three failures (1 attempt + 2 retries) the Job status shows `BackoffLimitExceeded`.

---

## Step 5 — Job with activeDeadlineSeconds

```bash
cat > deadline.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: too-slow
spec:
  activeDeadlineSeconds: 10
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: s
        image: busybox
        command: ["sh", "-c", "sleep 60"]
EOF
k apply -f deadline.yaml
sleep 15
k describe job too-slow | grep -A2 Conditions
```

`activeDeadlineSeconds` limits total Job wall-clock time. The Job is terminated with `DeadlineExceeded` regardless of `backoffLimit`.

---

## Step 6 — Clean up

```bash
k delete job hello pi-parallel must-fail too-slow --ignore-not-found
```

---

## Free online tools

- **Jobs concept doc**: https://kubernetes.io/docs/concepts/workloads/controllers/job/
- **batch/v1 API reference**: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `restartPolicy: Never` is mandatory in Job Pod templates.
- `completions` × `parallelism` controls throughput; `backoffLimit` controls fault tolerance.
- `activeDeadlineSeconds` is a hard wall-clock ceiling on the entire Job.
- Use `kubectl get job -w` to watch `COMPLETIONS` tick up in real time.
