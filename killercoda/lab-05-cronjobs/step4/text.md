# Step 4: Suspend and resume a CronJob

```bash
k patch cronjob report -p '{"spec":{"suspend":true}}'
k get cronjob report
k patch cronjob report -p '{"spec":{"suspend":false}}'
```

`SUSPEND = True` stops new Jobs but preserves history. Common exam task: "pause the CronJob without deleting it".

---
