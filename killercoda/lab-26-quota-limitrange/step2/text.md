# Step 2: Apply a ResourceQuota

```bash
cat > quota.yaml <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    pods: "5"
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
EOF
k apply -f quota.yaml
k describe quota team-a-quota -n team-a
```

`hard` sets the maximum totals. Once any value is reached, new Pods in the namespace are rejected.

---
