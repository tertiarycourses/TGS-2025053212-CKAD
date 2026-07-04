# Step 6: Observe ReplicaSet history

```bash
k get rs -l app=api
```

You should see two ReplicaSets: the old one at `0/0/0` and the new one at `2/2/2`. Deployments keep old ReplicaSets for rollback — the count kept is controlled by `revisionHistoryLimit` (default 10).

---
