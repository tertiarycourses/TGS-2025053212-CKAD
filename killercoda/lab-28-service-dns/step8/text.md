# Step 8: Clean up

```bash
k delete ns app probe
```

---

## Free online tools

- **DNS for Services and Pods**: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
- **CoreDNS docs**: https://coredns.io/docs/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- FQDN format: `<service>.<namespace>.svc.cluster.local`.
- Within the same namespace, the short name `<service>` resolves via the search list.
- Cross-namespace: use at minimum `<service>.<namespace>`.
- `ndots:5` explains why short names check the search list before doing absolute DNS.
- Headless Service (`clusterIP: None`) returns per-Pod IPs instead of a virtual IP.
