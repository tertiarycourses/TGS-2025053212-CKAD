# Step 7: Decommission blue after confidence

```bash
k delete deployment web-blue
k delete deployment web-green
k delete service web
```

---

## Free online tools

- **Deployment strategies overview**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Blue/Green = two Deployments with distinct `version` labels, one Service.
- Cutover is a `kubectl patch service` selector update — atomic and instant.
- Rollback is equally instant: patch the selector back to `version: blue`.
- Validate the new colour out-of-band (exec/curl) before flipping live traffic.
