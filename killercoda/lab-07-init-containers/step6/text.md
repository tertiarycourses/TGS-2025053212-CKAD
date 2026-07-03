# Step 6: Clean up

```bash
k delete pod web-init app-waiting --force --grace-period=0
k delete service db
```

---

## Free online tools

- **Init containers docs**: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
- **Pod lifecycle reference**: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Init containers run sequentially before any main container starts.
- Pod status `Init:N/M` means N of M init containers have completed.
- Common use cases: seed volumes, wait for DNS/service, one-time DB migration.
- If an init container fails, Kubernetes restarts it according to the Pod's `restartPolicy`.
