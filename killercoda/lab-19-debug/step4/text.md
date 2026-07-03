# Step 4: Diagnose: OOMKilled

```bash
cat > oom.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: hungry
spec:
  containers:
  - name: c
    image: polinux/stress
    command: ["stress"]
    args: ["--vm", "1", "--vm-bytes", "200M", "--vm-hang", "1"]
    resources:
      limits:
        memory: "64Mi"
EOF
k apply -f oom.yaml
sleep 15
k describe pod hungry | grep -A4 "Last State"
```

Look for `Reason: OOMKilled`. Resolution: increase the `memory` limit or reduce the workload's footprint.

---
