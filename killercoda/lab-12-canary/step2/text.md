# Step 2: Stable Deployment (90% of traffic)

```bash
cat > stable.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: web
      track: stable
  template:
    metadata:
      labels:
        app: web
        track: stable
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=stable"]
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
  - port: 5678
    targetPort: 5678
EOF
k apply -f stable.yaml
```

The Service selector uses only `app: web` — it routes to **both** stable and canary Pods. Traffic split is determined by replica count ratio.

---
