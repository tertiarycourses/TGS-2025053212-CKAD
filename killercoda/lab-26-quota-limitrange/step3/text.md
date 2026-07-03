# Step 3: Apply a LimitRange (defaults and maximums)

```bash
cat > limits.yaml <<'EOF'
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:
      cpu: 200m
      memory: 256Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    max:
      cpu: 500m
      memory: 512Mi
EOF
k apply -f limits.yaml
```

`default` = limit injected when the container has none. `defaultRequest` = request injected when missing. `max` = hard ceiling per container.

---
