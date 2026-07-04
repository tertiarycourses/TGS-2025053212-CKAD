# Step 5: Clean up

```bash
k delete pod scratch ramdisk host-peek --force --grace-period=0 --ignore-not-found
```

---

## Free online tools

- **Volumes docs**: https://kubernetes.io/docs/concepts/storage/volumes/
- **emptyDir reference**: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `emptyDir: {}` — ephemeral scratch space, shared by all containers in the Pod.
- `emptyDir.medium: Memory` — tmpfs-backed, fast, counted against container memory limits.
- `hostPath` — mounts from the node; avoid in production, useful in DaemonSets.
- Volumes are declared under `spec.volumes` and consumed via `spec.containers[].volumeMounts`.
