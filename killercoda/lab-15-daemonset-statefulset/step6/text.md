# Step 6: Scale a StatefulSet

```bash
k scale sts db --replicas=4
k get pods -l app=db -w
k scale sts db --replicas=2
```

Scale-down always terminates the highest ordinal first (`db-3`, then `db-2` if going to 2).

---
