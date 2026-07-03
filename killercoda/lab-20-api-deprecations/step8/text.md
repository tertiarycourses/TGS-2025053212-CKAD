# Step 8: Clean up

```bash
rm -f old.yaml
```

---

## Free online tools

- **API deprecation guide**: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
- **kubectl explain reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/
- **Kubernetes API reference (v1.35)**: https://kubernetes.io/docs/reference/kubernetes-api/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl api-resources` shows the correct `apiVersion` for every resource.
- `kubectl explain <resource>.<field>` is the exam-legal way to look up field names.
- `--recursive` on `explain` dumps the full schema tree — saves time on nested fields.
- Memorise the v1.35 stable API versions table above; deprecations are frequently tested.
