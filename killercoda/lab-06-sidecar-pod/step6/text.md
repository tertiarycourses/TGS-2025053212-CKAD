# Step 6: Clean up

```bash
k delete pod app-with-sidecar native-sidecar-pod --force --grace-period=0
```

---

## Free online tools

- **Sidecar pattern docs**: https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
- **Multi-container Pod docs**: https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Containers in the same Pod share the network namespace and optionally volumes.
- `kubectl logs -c <container>` and `kubectl exec -c <container>` for multi-container Pods.
- Native sidecars (Kubernetes 1.29+): `initContainer` with `restartPolicy: Always`.
- `emptyDir` is the standard glue volume between sidecar and main containers.
