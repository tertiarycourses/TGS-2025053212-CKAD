# Step 5: Preview without applying

```bash
kubectl kustomize overlays/dev | grep -E "name:|replicas:|image:"
kubectl kustomize overlays/prod | grep -E "name:|replicas:|image:"
```

Dev: name `dev-web`, 1 replica, `nginx:1.25`. Prod: name `prod-web`, 5 replicas, `nginx:1.26`.

---
