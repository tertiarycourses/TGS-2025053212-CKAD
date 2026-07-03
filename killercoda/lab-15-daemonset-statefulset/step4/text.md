# Step 4: StatefulSet with stable identities

```bash
cat > sts.yaml <<'EOF'
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: db
        image: busybox
        command: ["sh", "-c", "echo $(hostname) ready; sleep 3600"]
EOF
k apply -f sts.yaml
k rollout status sts/db
k get pods -l app=db
```

Pods are created in strict order: `db-0` → `db-1` → `db-2`. Deletion reverses the order: `db-2` → `db-1` → `db-0`.

---
