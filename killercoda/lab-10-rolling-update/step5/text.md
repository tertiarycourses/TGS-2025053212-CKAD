# Step 5: View rollout history

```bash
k rollout history deployment/web
k rollout history deployment/web --revision=2
```

Each `kubectl set image` or Pod-template mutation creates a new revision entry.

---
