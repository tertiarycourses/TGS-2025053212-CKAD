# Step 2: List every resource and its API group

```bash
k api-resources | head -20
k api-resources --namespaced=true | head -10
k api-resources --api-group=apps
k api-resources --api-group=batch
```

The `APIVERSION` column tells you exactly what to write in `apiVersion:` in your YAML.

---
