# Step 5: Inject an environment variable

```bash
k set env deployment/api APP_COLOR=blue
k describe deploy api | grep -A3 Environment
```

`kubectl set env` updates the Pod template, triggering a new ReplicaSet and a rolling update.

---
