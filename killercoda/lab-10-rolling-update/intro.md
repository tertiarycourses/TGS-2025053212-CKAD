# Lab 10 — Rolling Updates and Rollback

A Deployment performs zero-downtime upgrades by gradually replacing Pods one ReplicaSet at a time. CKAD 2026 tests `maxSurge`, `maxUnavailable`, ro...

**Lab environment:** [KillerCoda](https://killercoda.com/tertiary-labs-ckad/course/killercoda/lab-10-rolling-update)

A pre-built Kubernetes cluster (controlplane + node01) is ready to use — `kubectl` works immediately.
