# Step 7: Clean up

```bash
k delete ing demo
k delete svc web v2
k delete deployment web v2
k delete secret demo-tls
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml
rm -f tls.crt tls.key
```

---

## Free online tools

- **Ingress docs**: https://kubernetes.io/docs/concepts/services-networking/ingress/
- **ingress-nginx docs**: https://kubernetes.github.io/ingress-nginx/
- **Ingress controllers list**: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Ingress `apiVersion` is `networking.k8s.io/v1` (not `extensions/v1beta1` — removed in 1.22).
- `ingressClassName` selects which controller handles the Ingress.
- `tls.secretName` must point to a `kubernetes.io/tls` type Secret.
- `pathType: Prefix` matches the path and all sub-paths; `Exact` requires an exact match.
- `--resolve` and `-k` in curl allow testing Ingress without real DNS or a valid certificate.
