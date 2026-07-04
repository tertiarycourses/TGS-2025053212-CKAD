# Step 7: Clean up

```bash
k delete pod single bulk vol --force --grace-period=0
k delete cm app-cfg app-conf app-env
```

---

## Free online tools

- **ConfigMaps docs**: https://kubernetes.io/docs/concepts/configuration/configmap/
- **Configure Pods with ConfigMaps**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three ConfigMap creation methods: `--from-literal`, `--from-file`, `--from-env-file`.
- Three consumption methods: `configMapKeyRef` (single key), `envFrom` (all keys), volume mount (file).
- Volume-mounted ConfigMaps update live; env-var injections require a Pod restart.
- `configMapRef` in `envFrom` vs `configMapKeyRef` in `env.valueFrom` — know both spellings.
