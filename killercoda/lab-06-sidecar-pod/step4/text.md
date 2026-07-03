# Step 4: Exec into a specific container

```bash
k exec -it app-with-sidecar -c app -- sh -c 'ls /var/log; wc -l /var/log/app.log'
```

---
