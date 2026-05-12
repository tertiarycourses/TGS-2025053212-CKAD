# TGS-2025053212 — Certified Kubernetes Application Developer (CKAD) Hands-On Labs

> **Course:** WSQ — Certified Kubernetes Application Developer (CKAD) Training
> **Course Code:** TGS-2025053212
> **Register here:** https://www.tertiarycourses.com.sg/wsq-certified-kubernetes-application-developer-ckad-training.html

These are the official hands-on lab exercises for the WSQ Certified Kubernetes Application Developer (CKAD) Training course delivered by [**Tertiary Infotech Academy Pte Ltd**](https://www.tertiarycourses.com.sg/).

A complete set of **30 step-by-step labs** aligned to the CNCF **CKAD v1.35** exam objectives. Every lab runs on the free **Killercoda Kubernetes Playground** (https://killercoda.com/playgrounds/scenario/kubernetes) — no local install required.

Answer keys and reference material for the underlying exam objectives are maintained at https://github.com/ChathurangaVKD/ckad-exam-prep.

---

## How to use

1. Open the Killercoda Kubernetes playground in your browser: https://killercoda.com/playgrounds/scenario/kubernetes
2. Pick a lab from the list below and follow the steps in order.
3. Reset the playground between labs that change RBAC, NetworkPolicy, or cluster-scoped objects.
4. See [labs/tools.md](labs/tools.md) for every free tool used (with install commands and download links).

---

## Lab catalogue

### Domain 1 — Application Design and Build (20%)
- [Lab 1 — Build a Container Image with Docker](labs/lab-01-build-container-image.md)
- [Lab 2 — Multi-Stage Dockerfile](labs/lab-02-multistage-dockerfile.md)
- [Lab 3 — Create and Manage Pods](labs/lab-03-create-pods.md)
- [Lab 4 — Jobs (Run-to-Completion)](labs/lab-04-jobs.md)
- [Lab 5 — CronJobs (Scheduled Workloads)](labs/lab-05-cronjobs.md)
- [Lab 6 — Multi-Container Pods (Sidecar Pattern)](labs/lab-06-sidecar-pod.md)
- [Lab 7 — Init Containers](labs/lab-07-init-containers.md)
- [Lab 8 — Volumes (emptyDir and hostPath)](labs/lab-08-volumes.md)

### Domain 2 — Application Deployment (20%)
- [Lab 9 — Deployments and ReplicaSets](labs/lab-09-deployments.md)
- [Lab 10 — Rolling Updates and Rollback](labs/lab-10-rolling-update.md)
- [Lab 11 — Blue/Green Deployment](labs/lab-11-blue-green.md)
- [Lab 12 — Canary Deployment](labs/lab-12-canary.md)
- [Lab 13 — Helm Install and Upgrade](labs/lab-13-helm.md)
- [Lab 14 — Kustomize Overlays](labs/lab-14-kustomize.md)
- [Lab 15 — DaemonSets and StatefulSets](labs/lab-15-daemonset-statefulset.md)

### Domain 3 — Application Observability and Maintenance (15%)
- [Lab 16 — Liveness, Readiness and Startup Probes](labs/lab-16-probes.md)
- [Lab 17 — Container Logging](labs/lab-17-logging.md)
- [Lab 18 — kubectl top and Metrics](labs/lab-18-metrics.md)
- [Lab 19 — Debugging Pods and Events](labs/lab-19-debug.md)
- [Lab 20 — API Deprecations and kubectl explain](labs/lab-20-api-deprecations.md)

### Domain 4 — Application Environment, Configuration and Security (25%)
- [Lab 21 — ConfigMaps (env and volume)](labs/lab-21-configmaps.md)
- [Lab 22 — Secrets](labs/lab-22-secrets.md)
- [Lab 23 — SecurityContext](labs/lab-23-securitycontext.md)
- [Lab 24 — ServiceAccounts](labs/lab-24-serviceaccounts.md)
- [Lab 25 — RBAC (Role and RoleBinding)](labs/lab-25-rbac.md)
- [Lab 26 — ResourceQuota and LimitRange](labs/lab-26-quota-limitrange.md)

### Domain 5 — Services and Networking (20%)
- [Lab 27 — Services (ClusterIP, NodePort, LoadBalancer)](labs/lab-27-services.md)
- [Lab 28 — Service DNS](labs/lab-28-service-dns.md)
- [Lab 29 — Ingress with TLS](labs/lab-29-ingress-tls.md)
- [Lab 30 — NetworkPolicy](labs/lab-30-networkpolicy.md)

---

## Reference

- [labs/README.md](labs/README.md) — Lab index grouped by domain with software requirements
- [labs/tools.md](labs/tools.md) — Complete list of free tools (Killercoda + external)
- Exam prep & answer keys: https://github.com/ChathurangaVKD/ckad-exam-prep

---

## Free tools used

All tooling is **100% free**. Every lab runs inside the disposable Killercoda Kubernetes VM with `kubectl` and Docker pre-installed. Helm and Kustomize are installed in the relevant labs via free package managers.

Full tool list: [labs/tools.md](labs/tools.md).
