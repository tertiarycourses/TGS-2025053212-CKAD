# Step 7: Roll back to the previous revision

```bash
k rollout undo deployment/web
k rollout status deployment/web
k describe deployment web | grep Image:
```

To target a specific revision: `k rollout undo deployment/web --to-revision=1`

---
