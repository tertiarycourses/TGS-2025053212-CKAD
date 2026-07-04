# Step 3: Role: namespace-scoped permissions

```bash
k create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n dev
k describe role pod-reader -n dev
```

A `Role` is always scoped to one namespace. Verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, `deletecollection`.

---
