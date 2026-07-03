# Step 4: RoleBinding: link Role to ServiceAccount

```bash
k create rolebinding viewer-binding \
  --role=pod-reader \
  --serviceaccount=dev:viewer \
  -n dev
k describe rolebinding viewer-binding -n dev
```

---
