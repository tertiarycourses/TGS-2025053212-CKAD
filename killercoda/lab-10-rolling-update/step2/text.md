# Step 2: Create the initial Deployment

```bash
k create deployment web --image=nginx:1.24 --replicas=4
k rollout status deployment/web
```

---
