# Step 2: Create the backend Deployment

```bash
k create deployment web --image=nginx:1.25 --replicas=3
k get pods -l app=web
```

---
