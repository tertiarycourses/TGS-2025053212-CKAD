# Step 4: Failing Job and backoffLimit

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
