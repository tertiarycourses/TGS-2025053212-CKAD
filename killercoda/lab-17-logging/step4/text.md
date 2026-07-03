# Step 4: Retrieve logs from a crashed container

```bash
k run crasher --image=busybox --restart=Always -- sh -c 'echo about to die; sleep 3; exit 1'
sleep 25
k get pod crasher
k logs crasher --previous | head -5
```

`--previous` retrieves logs from the prior terminated container. This is the primary tool for diagnosing crash loops — the current container may have no logs yet.

---
