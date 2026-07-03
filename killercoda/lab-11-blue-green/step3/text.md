# Step 3: Deploy green (next version, no live traffic yet)

```bash
cat > green.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: green
  template:
    metadata:
      labels:
        app: web
        version: green
    spec:
      containers:
      - name: web
        image: nginx:1.25
EOF
k apply -f green.yaml
k get pods -l app=web --show-labels
```

Both colours are running. The Service selector still sends all traffic to `version: blue`.

---
