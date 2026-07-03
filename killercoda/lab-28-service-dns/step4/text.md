# Step 4: Resolve from a different namespace (needs namespace suffix)

```bash
k -n probe run client --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup web 2>&1 | head -2;
   nslookup web.app 2>&1 | head -2;
   nslookup web.app.svc.cluster.local | head -3'
```

Cross-namespace lookups require at least `<service>.<namespace>`. The FQDN always works.

---
