# Lab 4 — Jobs (Run-to-Completion)

A Job runs Pods until a target number of successful completions is reached. In this lab you will create a one-shot Job, a parallel Job, and a Job with retries on failure. CKAD frequently asks for `completions`, `parallelism` and `backoffLimit`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create a one-shot Job imperatively

```bash
alias k=kubectl
k create job hello --image=busybox -- echo "hello CKAD"
k get jobs,pods -l job-name=hello
k logs -l job-name=hello
```

---

## Step 2 — Parallel Job with multiple completions

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
        command: ["perl","-Mbignum=bpi","-wle","print bpi(50)"]
EOF
k apply -f parallel.yaml
k get jobs pi-parallel -w   # ctrl+C after Completions reaches 5/5
```

Field meaning:
- `completions: 5` — five successful Pods are required
- `parallelism: 2` — at most two Pods run at the same time
- `backoffLimit: 4` — four failures before the Job is marked failed

---

## Step 3 — Failing Job and backoffLimit

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
        command: ["sh","-c","exit 1"]
EOF
k apply -f fail.yaml
k get pods -l job-name=must-fail
```

After three failures (1 initial + 2 retries) the Job will report `BackoffLimitExceeded`.

---

## Step 4 — Job activeDeadlineSeconds

```bash
k delete job must-fail
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
        command: ["sh","-c","sleep 60"]
EOF
k apply -f deadline.yaml
sleep 15
k describe job too-slow | grep -A1 Conditions
```

The Job is terminated after 10 seconds with `Reason: DeadlineExceeded`.

---

## Step 5 — Clean up

```bash
k delete job hello pi-parallel too-slow
```

---

## What you learned
- The three core Job knobs: `completions`, `parallelism`, `backoffLimit`.
- `restartPolicy: Never` for Pod templates owned by Jobs.
- How `activeDeadlineSeconds` bounds total Job run-time.
