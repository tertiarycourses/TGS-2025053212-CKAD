# Step 6: Override the container command

```bash
k run sleeper --image=busybox --restart=Never -- sh -c 'sleep 3600'
k get pod sleeper
k logs sleeper || echo "no output — container is sleeping"
```

`--restart=Never` creates a bare Pod (not a Deployment). Everything after `--` becomes the container command and arguments.

---
