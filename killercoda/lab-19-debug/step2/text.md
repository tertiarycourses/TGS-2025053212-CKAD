# Step 2: Diagnose: ImagePullBackOff

```bash
k run typo --image=ngnix:1.25
sleep 20
k get pod typo
k describe pod typo | tail -15
```

Look for `Failed to pull image` in the Events section. The fix: delete and recreate with the correct image name.

```bash
k delete pod typo --force --grace-period=0
k run typo --image=nginx:1.25
```

---
