# Step 4: Verify the traffic split

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c \
  'for i in $(seq 1 30); do wget -qO- web:5678; done | sort | uniq -c'
```

Expected: approximately 27 `stable` and 3 `canary` lines.

---
