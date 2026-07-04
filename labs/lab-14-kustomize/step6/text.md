# Step 6: Apply the dev overlay

```bash
kubectl apply -k overlays/dev
kubectl get deploy,svc -l env=dev
```

---
