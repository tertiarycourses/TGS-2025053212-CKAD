# Lab 16 — Liveness, Readiness, and Startup Probes

Kubernetes uses three probes to manage container health: **livenessProbe** restarts a failed container, **readinessProbe** removes it from Service ...

**Lab environment:** [KillerCoda](https://killercoda.com/tertiarycourses/course/tertiary-labs/lab-16-probes)

A pre-built Kubernetes cluster (controlplane + node01) is ready to use — `kubectl` works immediately.
