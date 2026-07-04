# Step 5: LoadBalancer Service

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=LoadBalancer --name=web-lb
k get svc web-lb
```

On a cloud provider this provisions a public load balancer. On Killercoda, `EXTERNAL-IP` stays `<pending>` (no cloud LB controller). The NodePort it allocates is still usable.

---
