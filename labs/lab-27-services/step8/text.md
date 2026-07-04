# Step 8: Clean up

```bash
k delete svc web-cip web-np web-lb
k delete deployment web
```

---

## Free online tools

- **Services docs**: https://kubernetes.io/docs/concepts/services-networking/service/
- **kubectl expose reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_expose/
- **EndpointSlices docs**: https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ClusterIP` — in-cluster only; `NodePort` — every node gets a port; `LoadBalancer` — cloud LB.
- `kubectl expose deployment` is the fastest one-liner to create a Service.
- Empty `Endpoints` almost always means a selector label mismatch — check with `kubectl describe svc`.
- `kubectl get endpointslices` is the modern successor to `kubectl get endpoints`.
