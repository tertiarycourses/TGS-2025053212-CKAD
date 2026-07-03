# Step 2: Create ConfigMaps three ways

```bash
k create configmap app-cfg \
  --from-literal=COLOR=blue \
  --from-literal=GREETING=hello

cat > app.conf <<'EOF'
debug=true
log_level=info
EOF
k create configmap app-conf --from-file=app.conf

cat > env.list <<'EOF'
TIMEOUT=30
RETRIES=5
EOF
k create configmap app-env --from-env-file=env.list

k get cm
```

Three creation methods: `--from-literal` (key=value pairs), `--from-file` (file becomes a key), `--from-env-file` (dotenv format).

---
