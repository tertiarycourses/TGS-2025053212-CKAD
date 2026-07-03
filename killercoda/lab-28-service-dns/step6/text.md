# Step 6: Inspect /etc/resolv.conf inside a Pod

```bash
k -n app run shell --image=busybox --restart=Never -it --rm -- cat /etc/resolv.conf
```

Expected output:
```
nameserver 10.96.0.10
search app.svc.cluster.local svc.cluster.local cluster.local
ndots:5
```

`ndots:5` means any name with fewer than 5 dots triggers the search list first, then an absolute lookup. This is why `web` works within the namespace but `web.app` is needed cross-namespace.

---
