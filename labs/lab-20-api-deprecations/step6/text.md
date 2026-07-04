# Step 6: Look up the correct API version

```bash
k explain ingress --api-version=networking.k8s.io/v1 | head -10
k api-resources | grep -i ingress
```

This is the exam technique: when unsure of the `apiVersion`, run `api-resources` and read the `APIVERSION` column.

---
