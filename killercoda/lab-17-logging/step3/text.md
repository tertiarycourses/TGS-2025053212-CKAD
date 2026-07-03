# Step 3: Follow logs in real time

```bash
k logs -f noisy &
sleep 6
kill %1
```

`-f` streams new log lines as they are written — equivalent to `tail -f`.

---
