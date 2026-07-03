# Step 5: Drop Linux capabilities

```bash
cat > caps.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: caps
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
    securityContext:
      capabilities:
        drop: ["ALL"]
        add: ["NET_BIND_SERVICE"]
      allowPrivilegeEscalation: false
EOF
k apply -f caps.yaml
sleep 3
k exec caps -- sh -c 'cat /proc/1/status | grep Cap'
```

`drop: ["ALL"]` removes every Linux capability. `add` selectively restores only what is needed. `allowPrivilegeEscalation: false` prevents `setuid` binaries from gaining extra privileges.

---
