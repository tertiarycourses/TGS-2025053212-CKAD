# Step 6: Clean up

```bash
k delete cronjob date-printer report
k delete job report-manual --ignore-not-found
```

---

## Free online tools

- **CronJob docs**: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- **Cron syntax tester**: https://crontab.guru
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Standard cron syntax: `*/1 * * * *` = every minute.
- `concurrencyPolicy`: `Allow` (default) / `Forbid` / `Replace`.
- `timeZone` field is new in CKAD 2026 — always specify it in production.
- `kubectl create job --from=cronjob/<name>` triggers an immediate one-off run.
