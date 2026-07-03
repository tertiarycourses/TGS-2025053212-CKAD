# Step 6: kubectl debug: ephemeral container

```bash
k debug crash -it --image=busybox --target=crash -- sh -c 'ls /proc/1; echo inside-debug'
```

`kubectl debug` injects an **ephemeral container** into a running Pod — useful when the main container has no shell (distroless images). The ephemeral container shares the process namespace with the target.

---
