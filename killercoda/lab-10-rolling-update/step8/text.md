# Step 8: Clean up

```bash
k delete deployment web
```

---

## Free online tools

- **Rolling update docs**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment
- **kubectl rollout reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl set image` triggers a rolling update; `kubectl rollout status` watches it.
- `maxSurge` and `maxUnavailable` tune rollout speed vs. availability trade-off.
- `kubectl rollout pause` batches multiple changes into one ReplicaSet revision.
- `kubectl rollout undo` reverts to the previous (or specified) revision instantly.
