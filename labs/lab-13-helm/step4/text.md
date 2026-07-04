# Step 4: Inspect the generated manifests and values

```bash
helm get manifest web | head -40
helm get values web
```

`helm get manifest` shows the actual YAML Kubernetes received. `helm get values` shows what was overridden.

---
