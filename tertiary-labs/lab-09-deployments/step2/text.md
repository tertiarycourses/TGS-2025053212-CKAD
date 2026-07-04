# Step 2: Create a Deployment imperatively

```bash
k create deployment web --image=nginx:1.25 --replicas=3
k get deploy,rs,pod -l app=web
```

One command creates three resources: Deployment → ReplicaSet (hash-suffixed name) → 3 Pods. The chain is visible in the `-l app=web` output.

---
