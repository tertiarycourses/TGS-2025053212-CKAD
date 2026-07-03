# Step 7: Uninstall the release

```bash
helm uninstall web
helm list
```

---

## Free online tools

- **Helm docs**: https://helm.sh/docs/
- **Artifact Hub** — search public charts: https://artifacthub.io
- **Bitnami charts**: https://github.com/bitnami/charts
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Core Helm workflow: `repo add` → `install` → `upgrade` → `rollback` → `uninstall`.
- `--set` overrides chart values at install/upgrade time; `--reuse-values` preserves prior overrides.
- `helm history <release>` tracks every revision for audit and rollback.
- `helm get manifest` is the escape hatch to see what Helm actually sent to Kubernetes.
