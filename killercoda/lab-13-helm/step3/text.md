# Step 3: Install a release with value overrides

```bash
helm install web bitnami/nginx \
  --set service.type=ClusterIP \
  --set replicaCount=2
helm list
kubectl get pods -l app.kubernetes.io/instance=web
```

The release name `web` is what you reference for all subsequent commands. `--set key=value` overrides chart defaults.

---
