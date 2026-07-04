# Step 2: Create a noisy Pod and read its logs

```bash
k run noisy --image=busybox --restart=Never -- sh -c \
  'i=0; while true; do echo "line $i $(date)"; i=$((i+1)); sleep 1; done'
sleep 5
k logs noisy | tail -5
k logs noisy --tail=10
```

`--tail=N` limits output to the last N lines — useful when logs are very long.

---
