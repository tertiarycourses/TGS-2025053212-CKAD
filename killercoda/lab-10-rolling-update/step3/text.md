# Step 3: Tune the rolling-update strategy

```bash
k patch deployment web -p \
  '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":1}}}}'
k describe deployment web | grep -A4 RollingUpdateStrategy
```

- `maxSurge: 1` — at most 1 extra Pod above desired during the rollout
- `maxUnavailable: 1` — at most 1 Pod may be unavailable during the rollout

---
