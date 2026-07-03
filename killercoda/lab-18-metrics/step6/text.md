# Step 6: Clean up

```bash
k delete pod cpu-burner idle --force --grace-period=0
```

Leave metrics-server installed — it is used in Lab 26 (ResourceQuota).

---

## Free online tools

- **Metrics Server repo**: https://github.com/kubernetes-sigs/metrics-server
- **Resource management docs**: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl top` requires metrics-server to be installed and running.
- `--kubelet-insecure-tls` is needed on Killercoda due to self-signed certs.
- `kubectl top node` and `kubectl top pod --sort-by=cpu` are exam-day queries.
- `-A` flag covers all namespaces; combine with `| head` to manage output.
