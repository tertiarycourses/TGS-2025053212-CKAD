# Step 2: Create a CronJob imperatively

```bash
k create cronjob date-printer \
  --image=busybox \
  --schedule="*/1 * * * *" \
  -- sh -c "date; echo from cronjob"
k get cronjob date-printer
```

Wait 60 seconds, then verify Jobs are being spawned:

```bash
k get jobs
k logs -l job-name=$(k get jobs -o name | head -1 | cut -d/ -f2)
```

---
