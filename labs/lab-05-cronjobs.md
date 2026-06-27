# Lab 5 — CronJobs (Scheduled Workloads)

A CronJob creates Jobs on a time-based schedule using standard cron syntax. CKAD 2026 tests `concurrencyPolicy`, `startingDeadlineSeconds`, history limits, manual triggers, and suspend/resume. These fields appear verbatim in exam questions.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
```

---

## Step 2 — Create a CronJob imperatively

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

## Step 3 — Declarative CronJob with all key fields

```bash
cat > cron.yaml <<'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: report
spec:
  schedule: "*/2 * * * *"
  timeZone: "Asia/Singapore"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 30
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: report
            image: busybox
            command: ["sh", "-c", "echo report at $(date)"]
EOF
k apply -f cron.yaml
```

Field meanings (exam-tested):
- `timeZone` — CKAD 2026 addition; schedule interpreted in this timezone
- `concurrencyPolicy: Forbid` — skip a new run if the previous is still running
- `startingDeadlineSeconds: 30` — drop a missed schedule if more than 30s late
- `successfulJobsHistoryLimit: 2` — keep only 2 completed Job objects

---

## Step 4 — Suspend and resume a CronJob

```bash
k patch cronjob report -p '{"spec":{"suspend":true}}'
k get cronjob report
k patch cronjob report -p '{"spec":{"suspend":false}}'
```

`SUSPEND = True` stops new Jobs but preserves history. Common exam task: "pause the CronJob without deleting it".

---

## Step 5 — Trigger a CronJob manually (exam favourite)

```bash
k create job --from=cronjob/report report-manual
k logs -l job-name=report-manual
```

This is the answer whenever the exam asks: *"run this CronJob's workload immediately without waiting for the schedule"*.

---

## Step 6 — Clean up

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
