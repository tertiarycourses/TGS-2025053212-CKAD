# Step 3: Parallel Job with multiple completions

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
