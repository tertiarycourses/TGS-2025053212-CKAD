# Step 7: Clean up

```bash
k delete deployment web api
```

---

## Free online tools

- **Deployments docs**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- **kubectl set reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_set/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Deployment → ReplicaSet → Pod: the three-tier ownership chain.
- `kubectl scale` changes the replica count; the ReplicaSet controller acts immediately.
- `kubectl set env` / `kubectl set image` mutate the Pod template and trigger a rolling update.
- Old ReplicaSets are kept for rollback — `revisionHistoryLimit` controls how many.
