# Step 8: Clean up

```bash
k delete namespace team-a
```

---

## Free online tools

- **ResourceQuota docs**: https://kubernetes.io/docs/concepts/policy/resource-quotas/
- **LimitRange docs**: https://kubernetes.io/docs/concepts/policy/limit-range/
- **Resource units reference**: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ResourceQuota` limits **aggregate** usage in a namespace; exceeding it rejects new Pods.
- `LimitRange` enforces **per-container** minimums, maximums, and defaults.
- Without a LimitRange, Pods with no resource block cannot be created in a quota-enforced namespace.
- `kubectl describe quota` shows current `Used` vs `Hard` — the primary troubleshooting tool.
