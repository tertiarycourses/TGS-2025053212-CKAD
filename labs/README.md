# CKAD v1.35 — Lab Index

All labs run on the free Killercoda Kubernetes Playground:
**https://killercoda.com/playgrounds/scenario/kubernetes**

`kubectl`, `docker` and a single-node Kubernetes cluster are pre-installed inside the throw-away VM. Helm and Kustomize are installed in the labs that need them. Nothing has to be installed on your own machine.

---

## Domain 1 — Application Design and Build (20%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 1 | [Build a Container Image with Docker](lab-01-build-container-image.md) | `docker` (pre-installed) |
| 2 | [Multi-Stage Dockerfile](lab-02-multistage-dockerfile.md) | `docker` (pre-installed) |
| 3 | [Create and Manage Pods](lab-03-create-pods.md) | `kubectl` (pre-installed) |
| 4 | [Jobs (Run-to-Completion)](lab-04-jobs.md) | `kubectl` (pre-installed) |
| 5 | [CronJobs (Scheduled Workloads)](lab-05-cronjobs.md) | `kubectl` (pre-installed) |
| 6 | [Multi-Container Pods (Sidecar Pattern)](lab-06-sidecar-pod.md) | `kubectl` (pre-installed) |
| 7 | [Init Containers](lab-07-init-containers.md) | `kubectl` (pre-installed) |
| 8 | [Volumes (emptyDir and hostPath)](lab-08-volumes.md) | `kubectl` (pre-installed) |

## Domain 2 — Application Deployment (20%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 9 | [Deployments and ReplicaSets](lab-09-deployments.md) | `kubectl` (pre-installed) |
| 10 | [Rolling Updates and Rollback](lab-10-rolling-update.md) | `kubectl` (pre-installed) |
| 11 | [Blue/Green Deployment](lab-11-blue-green.md) | `kubectl` (pre-installed) |
| 12 | [Canary Deployment](lab-12-canary.md) | `kubectl` (pre-installed) |
| 13 | [Helm Install and Upgrade](lab-13-helm.md) | `helm` (curl install script in lab) |
| 14 | [Kustomize Overlays](lab-14-kustomize.md) | `kubectl` built-in `-k` |
| 15 | [DaemonSets and StatefulSets](lab-15-daemonset-statefulset.md) | `kubectl` (pre-installed) |

## Domain 3 — Application Observability and Maintenance (15%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 16 | [Liveness, Readiness and Startup Probes](lab-16-probes.md) | `kubectl` (pre-installed) |
| 17 | [Container Logging](lab-17-logging.md) | `kubectl` (pre-installed) |
| 18 | [kubectl top and Metrics](lab-18-metrics.md) | metrics-server (deployed in lab) |
| 19 | [Debugging Pods and Events](lab-19-debug.md) | `kubectl` (pre-installed) |
| 20 | [API Deprecations and kubectl explain](lab-20-api-deprecations.md) | `kubectl` (pre-installed) |

## Domain 4 — Application Environment, Configuration and Security (25%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 21 | [ConfigMaps (env and volume)](lab-21-configmaps.md) | `kubectl` (pre-installed) |
| 22 | [Secrets](lab-22-secrets.md) | `kubectl` (pre-installed) |
| 23 | [SecurityContext](lab-23-securitycontext.md) | `kubectl` (pre-installed) |
| 24 | [ServiceAccounts](lab-24-serviceaccounts.md) | `kubectl` (pre-installed) |
| 25 | [RBAC (Role and RoleBinding)](lab-25-rbac.md) | `kubectl` (pre-installed) |
| 26 | [ResourceQuota and LimitRange](lab-26-quota-limitrange.md) | `kubectl` (pre-installed) |

## Domain 5 — Services and Networking (20%)

| # | Lab | Free software needed |
|---|-----|----------------------|
| 27 | [Services (ClusterIP, NodePort, LoadBalancer)](lab-27-services.md) | `kubectl` (pre-installed) |
| 28 | [Service DNS](lab-28-service-dns.md) | `kubectl` (pre-installed) |
| 29 | [Ingress with TLS](lab-29-ingress-tls.md) | ingress-nginx (deployed in lab) |
| 30 | [NetworkPolicy](lab-30-networkpolicy.md) | Calico (already on Killercoda) |

---

## Suggested order

Work through Domain 1 → 2 → 3 → 4 → 5 in numeric order. Each lab is self-contained. Reset the Killercoda playground between labs that change cluster-scoped objects (RBAC, CRDs, NetworkPolicies, ingress controllers) to avoid carry-over.

## Exam-day kubectl aliases

Set these once at the top of every lab to mirror real exam conditions:

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
export now="--force --grace-period 0"
source <(kubectl completion bash)
complete -F __start_kubectl k
```
