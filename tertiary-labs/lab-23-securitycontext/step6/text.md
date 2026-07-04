# Step 6: Clean up

```bash
k delete pod nonroot enforced readonly caps --force --grace-period=0
```

---

## Free online tools

- **SecurityContext docs**: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- **Linux capabilities reference**: https://man7.org/linux/man-pages/man7/capabilities.7.html
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Pod-level `securityContext` applies to all containers; container-level overrides one.
- `runAsUser`, `runAsGroup`, `fsGroup` — control process and filesystem ownership.
- `runAsNonRoot: true` — blocks any image whose default user is root.
- `readOnlyRootFilesystem: true` + `capabilities.drop: ["ALL"]` + `allowPrivilegeEscalation: false` is the CKAD hardened container pattern.
