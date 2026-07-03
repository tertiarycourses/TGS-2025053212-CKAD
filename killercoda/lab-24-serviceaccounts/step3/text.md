# Step 3: Attach the ServiceAccount to a Pod

```bash
cat > pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  serviceAccountName: app-sa
  containers:
  - name: c
    image: bitnami/kubectl:latest
    command: ["sh", "-c", "sleep 3600"]
EOF
k apply -f pod.yaml
k get pod app -o jsonpath='{.spec.serviceAccountName}'; echo
```

---
