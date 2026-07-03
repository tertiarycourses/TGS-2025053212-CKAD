# Step 5: Exec probe + startupProbe for slow-starting apps

```bash
cat > slow-start.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: slow
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "sleep 20 && touch /tmp/ready && sleep 3600"]
    startupProbe:
      exec:
        command: ["cat", "/tmp/ready"]
      failureThreshold: 30
      periodSeconds: 5
    livenessProbe:
      exec:
        command: ["cat", "/tmp/ready"]
      periodSeconds: 10
EOF
k apply -f slow-start.yaml
k get pod slow -w
```

`startupProbe` runs exclusively until it succeeds. `failureThreshold: 30` × `periodSeconds: 5` = 150 seconds of startup budget before Kubernetes kills the container.

---
