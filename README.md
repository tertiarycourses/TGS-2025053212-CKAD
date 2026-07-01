# TGS-2025053212 — Certified Kubernetes Application Developer (CKAD) Hands-On Labs

> **Course:** WSQ — Certified Kubernetes Application Developer (CKAD) Training
> **Course Code:** TGS-2025053212
> **Register here:** https://www.tertiarycourses.com.sg/wsq-certified-kubernetes-application-developer-ckad-training.html

These are the official hands-on lab exercises for the WSQ Certified Kubernetes Application Developer (CKAD) Training course delivered by [**Tertiary Infotech Academy Pte Ltd**](https://www.tertiarycourses.com.sg/).

A complete set of **30 step-by-step labs** aligned to the CNCF **CKAD v1.35** exam objectives. Every lab runs on the free **Killercoda Kubernetes Playground** (https://killercoda.com/playgrounds/scenario/kubernetes) — no local install required.

---

## How to use

1. Open the Killercoda Kubernetes playground in your browser: https://killercoda.com/playgrounds/scenario/kubernetes
2. Pick a lab from the list below and follow the steps in order.
3. Reset the playground between labs that change RBAC, NetworkPolicy, or cluster-scoped objects.
4. See [labs/tools.md](labs/tools.md) for every free tool used (with install commands and download links).

---

## Lab catalogue

### Domain 1 — Application Design and Build (20%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [01](labs/lab-01-build-container-image/) | Build a Container Image | Dockerfile, `docker build`, `docker run` |
| [02](labs/lab-02-multistage-dockerfile/) | Multi-Stage Dockerfile | Build-time deps vs runtime image, layer caching |
| [03](labs/lab-03-create-pods/) | Create and Manage Pods | `kubectl run`, Pod spec, `exec`, `logs` |
| [04](labs/lab-04-jobs/) | Jobs (Run-to-Completion) | `completions`, `parallelism`, backoff limits |
| [05](labs/lab-05-cronjobs/) | CronJobs | Cron schedule, concurrencyPolicy, `kubectl create cronjob` |
| [06](labs/lab-06-sidecar-pod/) | Multi-Container Pods (Sidecar) | Shared volumes, log-forwarder pattern |
| [07](labs/lab-07-init-containers/) | Init Containers | Sequencing, dependency gates, `initContainers` spec |
| [08](labs/lab-08-volumes/) | Volumes | emptyDir, hostPath, volume mounts |

### Domain 2 — Application Deployment (20%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [09](labs/lab-09-deployments/) | Deployments and ReplicaSets | Create, scale, inspect |
| [10](labs/lab-10-rolling-update/) | Rolling Updates and Rollback | `kubectl set image`, `rollout status`, `rollout undo` |
| [11](labs/lab-11-blue-green/) | Blue/Green Deployment | Service selector switch, zero-downtime |
| [12](labs/lab-12-canary/) | Canary Deployment | Weighted traffic split with Deployments |
| [13](labs/lab-13-helm/) | Helm Install and Upgrade | `helm install`, `upgrade`, `rollback`, `values.yaml` |
| [14](labs/lab-14-kustomize/) | Kustomize Overlays | Base + overlays, `kustomization.yaml`, `kubectl apply -k` |
| [15](labs/lab-15-daemonset-statefulset/) | DaemonSets and StatefulSets | Node-per-pod, ordered identity, stable storage |

### Domain 3 — Application Observability and Maintenance (15%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [16](labs/lab-16-probes/) | Liveness, Readiness & Startup Probes | HTTP, exec, TCP probes; restart behaviour |
| [17](labs/lab-17-logging/) | Container Logging | `kubectl logs`, multi-container, previous crash logs |
| [18](labs/lab-18-metrics/) | kubectl top and Metrics Server | `kubectl top pod/node`, resource usage |
| [19](labs/lab-19-debug/) | Debugging Pods and Events | `describe`, Events, ephemeral debug containers |
| [20](labs/lab-20-api-deprecations/) | API Deprecations | `kubectl explain`, deprecation warnings, version pinning |

### Domain 4 — Application Environment, Configuration and Security (25%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [21](labs/lab-21-configmaps/) | ConfigMaps | env var injection, volume mount |
| [22](labs/lab-22-secrets/) | Secrets | Opaque, TLS, imagePullSecret types |
| [23](labs/lab-23-securitycontext/) | SecurityContext | runAsUser, readOnlyRootFilesystem, capabilities |
| [24](labs/lab-24-serviceaccounts/) | ServiceAccounts | Auto-mount, token projection |
| [25](labs/lab-25-rbac/) | RBAC | Role, ClusterRole, RoleBinding, `can-i` |
| [26](labs/lab-26-quota-limitrange/) | ResourceQuota and LimitRange | Namespace limits, default requests |

### Domain 5 — Services and Networking (20%)

| Lab | Topic | What you practise |
|-----|-------|-------------------|
| [27](labs/lab-27-services/) | Services (ClusterIP, NodePort, LoadBalancer) | Service types, port mapping, selectors |
| [28](labs/lab-28-service-dns/) | Service DNS | CoreDNS, FQDN resolution, headless services |
| [29](labs/lab-29-ingress-tls/) | Ingress with TLS | ingress-nginx, self-signed cert, TLS termination |
| [30](labs/lab-30-networkpolicy/) | NetworkPolicy | Ingress/egress rules, namespace selectors, deny-all |

---

## Practicums

Hands-on practicum exercises, one per training day:

| Practicum | Coverage | Time |
|-----------|----------|------|
| [Practicum 1](labs/practicums/practicum-1/question.md) | Domain 1 — Application Design & Build | 45 min |
| [Practicum 2](labs/practicums/practicum-2/question.md) | Domain 2 — Application Deployment | 45 min |
| [Practicum 3](labs/practicums/practicum-3/question.md) | Domains 3 & 4 — Observability, Config & Security | 45 min |
| [Practicum 4](labs/practicums/practicum-4/question.md) | Domain 5 + Final Mock (all domains) | 2 hr |

---

## Courseware

The [`courseware/`](courseware/) folder holds the generated training deliverables (Version 1.0):

| File | Description |
|------|-------------|
| [`CKAD-Certified-Kubernetes-Application-Developer-v1.0.pptx`](courseware/CKAD-Certified-Kubernetes-Application-Developer-v1.0.pptx) | Slide deck — 344 slides, all 4 days (includes an online practice-exam slide) |
| [`CKAD-Certified-Kubernetes-Application-Developer-v1.0.pdf`](courseware/CKAD-Certified-Kubernetes-Application-Developer-v1.0.pdf) | PDF version of the slide deck |
| [`LG-Certified-Kubernetes-Application-Developer-CKAD.docx`](courseware/LG-Certified-Kubernetes-Application-Developer-CKAD.docx) · [PDF](courseware/LG-Certified-Kubernetes-Application-Developer-CKAD.pdf) | Learner Guide (Word + PDF) |
| [`LP-Certified-Kubernetes-Application-Developer-CKAD.docx`](courseware/LP-Certified-Kubernetes-Application-Developer-CKAD.docx) · [PDF](courseware/LP-Certified-Kubernetes-Application-Developer-CKAD.pdf) | Lesson Plan (Word + PDF) — day schedule with per-session slide page references |

Courseware is generated from single-source scripts in [`.claude/skills/`](.claude/skills/) (Tertiary Infotech WSQ house skills for slides, Learner Guide, Lesson Plan and assessments).

---

## Reference

- [labs/README.md](labs/README.md) — Lab index grouped by domain with software requirements
- [labs/tools.md](labs/tools.md) — Complete list of free tools (Killercoda + external)
- CNCF CKAD exam curriculum: https://github.com/cncf/curriculum
- Exam prep & answer keys: https://github.com/ChathurangaVKD/ckad-exam-prep
