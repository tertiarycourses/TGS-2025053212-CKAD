# Step 3: Headless Service for the StatefulSet

```bash
cat > headless.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: db
spec:
  clusterIP: None
  selector:
    app: db
  ports:
  - port: 5432
    name: pg
EOF
k apply -f headless.yaml
```

`clusterIP: None` makes this headless — DNS returns individual Pod IPs, not a virtual IP.

---
