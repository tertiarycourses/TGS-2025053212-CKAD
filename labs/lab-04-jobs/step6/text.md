# Step 6: Clean up

```bash
k delete job hello pi-parallel must-fail too-slow --ignore-not-found
```

---

## Free online tools

- **Jobs concept doc**: https://kubernetes.io/docs/concepts/workloads/controllers/job/
- **batch/v1 API reference**: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `restartPolicy: Never` is mandatory in Job Pod templates.
- `completions` × `parallelism` controls throughput; `backoffLimit` controls fault tolerance.
- `activeDeadlineSeconds` is a hard wall-clock ceiling on the entire Job.
- Use `kubectl get job -w` to watch `COMPLETIONS` tick up in real time.
