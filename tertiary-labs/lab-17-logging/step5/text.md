# Step 5: Multi-container Pod logs

```bash
cat > multi.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: multi
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "while true; do echo APP $(date); sleep 1; done"]
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "while true; do echo SIDE $(date); sleep 1; done"]
EOF
k apply -f multi.yaml
sleep 5
k logs multi -c app | head -3
k logs multi -c sidecar | head -3
k logs multi --all-containers=true --prefix=true | head -8
```

`--prefix=true` adds `[pod/container]` labels to every line — essential when tailing multiple containers.

---
