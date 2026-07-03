# Step 3: Scale up and down

```bash
k scale deployment web --replicas=5
k get pods -l app=web
k scale deployment web --replicas=2
k get pods -l app=web
```

The ReplicaSet controller reconciles the actual count to match desired at all times.

---
