# Step 2: Init container that seeds the web root

```bash
cat > init.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web-init
spec:
  volumes:
  - name: html
    emptyDir: {}
  initContainers:
  - name: seed
    image: busybox
    command: ["sh", "-c", "echo '<h1>Seeded by init container</h1>' > /work/index.html"]
    volumeMounts:
    - name: html
      mountPath: /work
  containers:
  - name: web
    image: nginx:1.25
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
EOF
k apply -f init.yaml
k get pod web-init
```

While the init container runs you see `Init:0/1`. After it exits 0, the main container starts and status becomes `Running`.

---
