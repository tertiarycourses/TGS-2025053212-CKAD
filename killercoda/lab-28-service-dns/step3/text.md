# Step 3: Resolve from the same namespace (short name)

```bash
k -n app run client --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup web; wget -qO- web | head -3'
```

Within the same namespace, `web` resolves because the Pod's search domain includes `app.svc.cluster.local`.

---
