# Step 5: Upgrade the release

```bash
helm upgrade web bitnami/nginx --set replicaCount=4 --reuse-values
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

`--reuse-values` preserves the prior `service.type=ClusterIP` setting while only changing `replicaCount`.

---
