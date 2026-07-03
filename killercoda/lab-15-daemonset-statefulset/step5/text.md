# Step 5: Verify stable per-Pod DNS

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup db-0.db.default.svc.cluster.local; nslookup db.default.svc.cluster.local'
```

`db-0.db.default.svc.cluster.local` resolves to one Pod's IP. The headless Service DNS returns all three.

---
