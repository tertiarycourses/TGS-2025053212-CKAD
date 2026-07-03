# Step 5: Unblock the init container by creating the Service

```bash
k create service clusterip db --tcp=5432:5432
k get pod app-waiting -w
```

Once CoreDNS can resolve `db.default.svc.cluster.local`, the init container exits and the main container starts. Press Ctrl+C after status shows `Running`.

---
