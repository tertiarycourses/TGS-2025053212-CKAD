# Step 3: Canary Deployment (10% of traffic)

```bash
cat > canary.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
      track: canary
  template:
    metadata:
      labels:
        app: web
        track: canary
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=canary"]
EOF
k apply -f canary.yaml
k get pods -l app=web --show-labels
```

9 stable + 1 canary = roughly 10% of requests hit the canary.

---
