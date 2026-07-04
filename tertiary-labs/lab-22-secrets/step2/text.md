# Step 2: Create a generic Secret

```bash
k create secret generic db-cred \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASS=s3cr3t
k get secret db-cred -o yaml
```

Values are base64-encoded (not encrypted). Anyone with `get secret` RBAC can decode them.

---
