# Step 4: Prod overlay (5 replicas, image bump to 1.26)

```bash
cat > overlays/prod/replica-patch.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 5
EOF

cat > overlays/prod/kustomization.yaml <<'EOF'
resources:
- ../../base
namePrefix: prod-
commonLabels:
  env: prod
images:
- name: nginx
  newTag: "1.26"
patches:
- path: replica-patch.yaml
EOF
```

---
