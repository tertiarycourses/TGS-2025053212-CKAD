# Step 3: Inject a single key as an environment variable

```bash
cat > pod-single.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: single
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "echo COLOR=$COLOR; sleep 3600"]
    env:
    - name: COLOR
      valueFrom:
        configMapKeyRef:
          name: app-cfg
          key: COLOR
EOF
k apply -f pod-single.yaml
sleep 3
k logs single
```

Expected: `COLOR=blue`

---
