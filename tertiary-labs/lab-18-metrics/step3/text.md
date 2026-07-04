# Step 3: Generate CPU load

```bash
k run cpu-burner --image=busybox -- sh -c 'while true; do :; done'
k run idle --image=busybox -- sh -c 'sleep 3600'
sleep 30
```

Wait 30 seconds for metrics to scrape the new Pods.

---
