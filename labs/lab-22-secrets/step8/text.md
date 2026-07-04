# Step 8: Clean up

```bash
k delete pod client vol --force --grace-period=0
k delete secret db-cred demo-tls myreg
rm -f tls.crt tls.key
```

---

## Free online tools

- **Secrets docs**: https://kubernetes.io/docs/concepts/configuration/secret/
- **Secret types reference**: https://kubernetes.io/docs/concepts/configuration/secret/#secret-types
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three Secret types: `generic`, `tls` (`kubernetes.io/tls`), `docker-registry`.
- `envFrom: secretRef` injects all keys; `env.valueFrom.secretKeyRef` injects one key.
- Volume mount with `defaultMode: 0400` is exam-tested — restricts file to owner read-only.
- Secrets are base64-encoded, not encrypted — use RBAC to restrict access.
