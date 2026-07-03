# Step 7: Clean up

```bash
k delete pod noisy crasher multi --force --grace-period=0
k delete deployment fleet
```

---

## Free online tools

- **kubectl logs reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/
- **Logging architecture**: https://kubernetes.io/docs/concepts/cluster-administration/logging/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl logs --tail=N` for recent lines; `-f` for live streaming.
- `--previous` is the key to diagnosing CrashLoopBackOff pods.
- `-c <container>` selects a specific container in a multi-container Pod.
- `-l <selector>` aggregates logs from all matching Pods simultaneously.
