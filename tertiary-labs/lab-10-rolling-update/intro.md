# Lab 10 — Rolling Updates and Rollback

A Deployment performs zero-downtime upgrades by gradually replacing Pods one ReplicaSet at a time. CKAD 2026 tests `maxSurge`, `maxUnavailable`, ro...

**Lab environment:** [KillerCoda](https://killercoda.com/tertiarycourses/course/tertiary-labs/lab-10-rolling-update)

A pre-built Kubernetes cluster (controlplane + node01) is ready to use — `kubectl` works immediately.
