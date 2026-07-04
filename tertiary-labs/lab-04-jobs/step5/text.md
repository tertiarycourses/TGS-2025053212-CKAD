# Step 5: Job with activeDeadlineSeconds

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
