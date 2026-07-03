# Step 7: Apply the prod overlay and verify image

```bash
kubectl apply -k overlays/prod
kubectl get deploy,svc -l env=prod
kubectl describe deploy prod-web | grep Image:
```

---
