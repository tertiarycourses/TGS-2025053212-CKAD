# Step 3: Decode a Secret value

```bash
k get secret db-cred -o jsonpath='{.data.DB_PASS}' | base64 -d; echo
```

Expected: `s3cr3t`

---
