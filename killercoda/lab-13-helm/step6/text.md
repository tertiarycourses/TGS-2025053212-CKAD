# Step 6: Roll back to revision 1

```bash
helm rollback web 1
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

`helm history` lists every revision with its status. Rollback creates a new revision — it does not delete history.

---
