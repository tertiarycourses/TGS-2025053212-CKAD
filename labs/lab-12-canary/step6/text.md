# Step 6: Clean up

```bash
k delete deployment web-stable web-canary --ignore-not-found
k delete service web
```

---

## Free online tools

- **Canary deployments on Kubernetes**: https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#canary-deployments
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Canary = two Deployments with different `track` labels behind one broad Service selector.
- Traffic split is approximated by replica ratio (9:1 ≈ 90%/10%).
- Promotion is `kubectl scale` on both Deployments — no Service change needed.
- For precise percentage splits, use a service mesh (Istio/Linkerd) — beyond CKAD scope.
