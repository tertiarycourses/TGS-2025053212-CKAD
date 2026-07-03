# Step 5: Flip the Service to green (atomic cutover)

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'
k describe svc web | grep Selector
```

All traffic now routes to green Pods. Blue Pods are still running as an instant fallback.

---
