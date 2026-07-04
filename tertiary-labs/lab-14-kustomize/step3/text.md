# Step 3: Dev overlay (1 replica, `dev-` name prefix)

```bash
cat > overlays/dev/kustomization.yaml <<'EOF'
resources:
- ../../base
namePrefix: dev-
commonLabels:
  env: dev
EOF
```

---
