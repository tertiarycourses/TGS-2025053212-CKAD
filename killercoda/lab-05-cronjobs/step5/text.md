# Step 5: Trigger a CronJob manually (exam favourite)

```bash
k create job --from=cronjob/report report-manual
k logs -l job-name=report-manual
```

This is the answer whenever the exam asks: *"run this CronJob's workload immediately without waiting for the schedule"*.

---
