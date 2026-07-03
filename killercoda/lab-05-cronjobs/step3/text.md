# Step 3: Declarative CronJob with all key fields

```bash
cat > cron.yaml <<'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: report
spec:
  schedule: "*/2 * * * *"
  timeZone: "Asia/Singapore"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 30
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: report
            image: busybox
            command: ["sh", "-c", "echo report at $(date)"]
EOF
k apply -f cron.yaml
```

Field meanings (exam-tested):
- `timeZone` — CKAD 2026 addition; schedule interpreted in this timezone
- `concurrencyPolicy: Forbid` — skip a new run if the previous is still running
- `startingDeadlineSeconds: 30` — drop a missed schedule if more than 30s late
- `successfulJobsHistoryLimit: 2` — keep only 2 completed Job objects

---
