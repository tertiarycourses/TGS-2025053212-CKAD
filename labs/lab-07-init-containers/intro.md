# Lab 7 — Init Containers

Init containers run **in order, to completion**, before any main container starts. Use them to seed shared volumes, wait for upstream services, or ...

**Lab environment:** [KillerCoda](https://killercoda.com/tertiarycourses/course/labs/lab-07-init-containers)

A pre-built Kubernetes cluster (controlplane + node01) is ready to use — `kubectl` works immediately.
