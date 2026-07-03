# Step 5: Validate with kubectl auth can-i

```bash
k auth can-i list pods   -n dev     --as=system:serviceaccount:dev:viewer
k auth can-i delete pods -n dev     --as=system:serviceaccount:dev:viewer
k auth can-i list pods   -n default --as=system:serviceaccount:dev:viewer
```

Expected: `yes`, `no`, `no`. The Role only covers the `dev` namespace.

---
