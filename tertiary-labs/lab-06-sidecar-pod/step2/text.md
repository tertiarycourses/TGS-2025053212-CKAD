# Step 2: Sidecar that tails a shared log file

```bash
cat > sidecar.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  volumes:
  - name: logs
    emptyDir: {}
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "i=0; while true; do echo \"$(date) line $i\" >> /var/log/app.log; i=$((i+1)); sleep 2; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
  - name: log-shipper
    image: busybox
    command: ["sh", "-c", "tail -F /var/log/app.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
EOF
k apply -f sidecar.yaml
k get pod app-with-sidecar
```

The shared `emptyDir` is the glue: `app` writes, `log-shipper` reads — both see `/var/log`.

---
