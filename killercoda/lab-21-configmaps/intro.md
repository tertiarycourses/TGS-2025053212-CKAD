# Lab 21 — ConfigMaps (Environment and Volume Injection)

ConfigMaps inject non-secret configuration into Pods. CKAD 2026 tests all three injection styles: individual env vars (`valueFrom.configMapKeyRef`)...

**Lab environment:** [KillerCoda](https://killercoda.com/tertiarycourses/course/killercoda/lab-21-configmaps)

A pre-built Kubernetes cluster (controlplane + node01) is ready to use — `kubectl` works immediately.
