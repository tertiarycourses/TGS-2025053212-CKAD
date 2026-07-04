# Step 2: HTTP liveness + readiness probe

```bash
cat > http-probes.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web-probes
  labels:
    app: web
spec:
  containers:
  - name: web
    image: nginx:1.25
    ports:
    - containerPort: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 2
      periodSeconds: 5
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 3
EOF
k apply -f http-probes.yaml
k get pod web-probes -w
```

Wait until `READY 1/1` then press Ctrl+C.

---
