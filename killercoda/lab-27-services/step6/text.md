# Step 6: EndpointSlices

```bash
k get endpoints web-cip
k get endpointslices -l kubernetes.io/service-name=web-cip
```

EndpointSlices (v1.21+) are the successor to Endpoints. Both are updated whenever Pods are added or removed.

---
