# Lab 5 — CronJobs (Scheduled Workloads)

A CronJob creates Jobs on a time-based schedule. In this lab you will create a CronJob that prints the date every minute, then tune `concurrencyPolicy`, `successfulJobsHistoryLimit`, and `startingDeadlineSeconds`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Imperative CronJob

```bash
alias k=kubectl
k create cronjob date-printer --image=busybox --schedule="*/1 * * * *" -- sh -c "date; echo from cronjob"
k get cronjob
```

Wait one minute then verify Jobs are being created:

```bash
k get jobs
k logs -l job-name=$(k get jobs -o name | head -1 | cut -d/ -f2)
```

---

## Step 2 — Declarative CronJob with full options

```bash
cat > cron.yaml <<'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: report
spec:
  schedule: "*/2 * * * *"
  concurrencyPolicy: Forbid          # do not start a new Job if previous is still running
  successfulJobsHistoryLimit: 2      # keep only 2 completed Job histories
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
            command: ["sh","-c","echo report at $(date)"]
EOF
k apply -f cron.yaml
```

Key options:
- `concurrencyPolicy: Allow | Forbid | Replace`
- `startingDeadlineSeconds` — drop missed schedules older than this many seconds
- `successfulJobsHistoryLimit` — clean up old Job objects automatically

---

## Step 3 — Suspend and resume

```bash
k patch cronjob report -p '{"spec":{"suspend":true}}'
k get cronjob report                  # SUSPEND column = True
k patch cronjob report -p '{"spec":{"suspend":false}}'
```

A suspended CronJob will not create new Jobs but keeps its existing history.

---

## Step 4 — Trigger a CronJob manually

```bash
k create job --from=cronjob/report report-manual
k logs -l job-name=report-manual
```

This is the answer to the common exam question *"run a CronJob's payload immediately"*.

---

## Step 5 — Clean up

```bash
k delete cronjob date-printer report
k delete job report-manual --ignore-not-found
```

---

## What you learned
- Standard cron syntax `*/1 * * * *`.
- `concurrencyPolicy` and history limits.
- Manual one-off run with `kubectl create job --from=cronjob/<name>`.
