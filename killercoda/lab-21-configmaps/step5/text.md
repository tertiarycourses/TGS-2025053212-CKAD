# Step 5: Mount a ConfigMap as a file volume

```bash
cat > pod-vol.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: vol
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "cat /etc/app/app.conf; sleep 3600"]
    volumeMounts:
    - name: cfg
      mountPath: /etc/app
  volumes:
  - name: cfg
    configMap:
      name: app-conf
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
```

Each key in the ConfigMap becomes a file in the mounted directory.

---
