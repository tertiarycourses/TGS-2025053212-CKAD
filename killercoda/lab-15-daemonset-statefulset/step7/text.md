# Step 7: Clean up

```bash
k delete ds node-agent
k delete sts db
k delete svc db
```

---

## Free online tools

- **DaemonSet docs**: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
- **StatefulSet docs**: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- DaemonSet = one Pod per matching node; `tolerations` control which nodes are included.
- StatefulSet = stable Pod names (`<name>-0`, `<name>-1`) and ordered start/stop.
- Headless Service (`clusterIP: None`) is required for per-Pod DNS in a StatefulSet.
- Scale-down order is always highest ordinal first.
