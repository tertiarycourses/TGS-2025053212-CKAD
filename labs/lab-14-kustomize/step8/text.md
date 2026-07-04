# Step 8: Clean up

```bash
kubectl delete -k overlays/dev
kubectl delete -k overlays/prod
```

---

## Free online tools

- **Kustomize docs**: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- **Kustomize reference site**: https://kustomize.io
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Base + overlays = reuse without Go templating.
- `namePrefix` and `commonLabels` are applied to every resource in the overlay.
- `images` block overrides image tags without editing base files.
- `kubectl apply -k` and `kubectl kustomize` are built into kubectl — no extra binary.
