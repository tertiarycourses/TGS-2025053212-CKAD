# Step 6: Pause, apply multiple changes, then resume

```bash
k rollout pause deployment/web
k set image deployment/web nginx=nginx:1.26
k set env deployment/web APP_ENV=production
k rollout resume deployment/web
k rollout status deployment/web
```

Pausing batches multiple mutations into a single new ReplicaSet — one rollout, not two.

---
