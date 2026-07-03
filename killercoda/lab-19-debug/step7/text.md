# Step 7: Clean up

```bash
k delete pod typo crash hungry --force --grace-period=0 --ignore-not-found
```

---

## Free online tools

- **Debugging Pods docs**: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
- **kubectl debug reference**: https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ImagePullBackOff` → wrong image name or tag; fix with `kubectl delete` + `kubectl run`.
- `CrashLoopBackOff` → container exits non-zero; use `kubectl logs --previous`.
- `OOMKilled` → container exceeded memory limit; raise `resources.limits.memory`.
- `kubectl get events --sort-by=.lastTimestamp` is faster than `describe` for cluster-wide diagnosis.
- `kubectl debug` injects an ephemeral shell into any running Pod.
