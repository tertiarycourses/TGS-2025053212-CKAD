# Step 5: Violate the LimitRange maximum

```bash
k run big --image=nginx:1.25 -n team-a \
  --overrides='{"spec":{"containers":[{"name":"big","image":"nginx:1.25","resources":{"limits":{"cpu":"1","memory":"1Gi"}}}]}}' \
  2>&1 | head -5
```

Rejected: `maximum cpu usage per Container is 500m`. The LimitRange enforced the `max` ceiling.

---
