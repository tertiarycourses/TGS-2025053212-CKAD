# Step 7: Docker registry Secret

```bash
k create secret docker-registry myreg \
  --docker-server=registry.example.com \
  --docker-username=myuser \
  --docker-password=mypass \
  --docker-email=myuser@example.com
k get secret myreg -o jsonpath='{.type}'; echo
```

Reference in a Pod: `spec.imagePullSecrets: [{name: myreg}]`.

---
