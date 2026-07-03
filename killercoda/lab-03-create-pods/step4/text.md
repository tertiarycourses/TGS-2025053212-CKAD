# Step 4: Add a label and apply the manifest

```bash
sed -i 's/^  labels:.*/  labels:\n    tier: frontend/' web2.yaml
k apply -f web2.yaml
k get pod web2 --show-labels
```

`kubectl apply` is idempotent — safe to run multiple times.

---
