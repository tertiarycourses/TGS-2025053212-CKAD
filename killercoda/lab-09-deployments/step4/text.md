# Step 4: Generate Deployment YAML and apply

```bash
k create deployment api --image=httpd:2.4 --replicas=2 $do > api.yaml
cat api.yaml
k apply -f api.yaml
```

Generate → inspect → apply is the safe CKAD workflow for any new resource.

---
