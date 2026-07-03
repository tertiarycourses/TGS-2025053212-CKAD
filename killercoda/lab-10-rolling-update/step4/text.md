# Step 4: Trigger an image update and watch the rollout

```bash
k set image deployment/web nginx=nginx:1.25
k rollout status deployment/web
k get rs -l app=web
```

Watch the old ReplicaSet drain to 0 while the new one ramps to 4.

---
