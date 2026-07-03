# Step 7: Clean up

```bash
k delete pod web web2 sleeper --force --grace-period=0
```

`--force --grace-period=0` skips the 30-second termination grace period — use this in the exam to save time.

---

## Free online tools

- **kubectl cheat sheet** (allowed in exam): https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **killer.sh** — CKAD mock exam simulator: https://killer.sh
- **JSONPath reference**: https://kubernetes.io/docs/reference/kubectl/jsonpath/
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `alias k=kubectl` and `export do="--dry-run=client -o yaml"` — set these first on exam day.
- `kubectl run` for imperative Pods; `kubectl apply -f` for declarative manifests.
- `--restart=Never` + `--` separator for bare Pods with custom commands.
- `kubectl describe` for events; `jsonpath` for field extraction.
