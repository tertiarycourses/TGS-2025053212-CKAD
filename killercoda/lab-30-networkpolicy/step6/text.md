# Step 6: Clean up

```bash
k delete ns secured trusted
```

---

## Free online tools

- **NetworkPolicy docs**: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- **NetworkPolicy editor** (visual): https://editor.networkpolicy.io
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Default-deny pattern: `podSelector: {}` + `policyTypes: [Ingress]` with no `ingress:` list.
- `podSelector` in `ingress.from` matches Pods by label within the same namespace.
- `namespaceSelector` in `ingress.from` matches all Pods in matching namespaces.
- Egress works the same way — the common exam pattern is "deny all egress except DNS (port 53)".
- NetworkPolicies are additive: multiple policies combine with logical OR on the allow rules.
