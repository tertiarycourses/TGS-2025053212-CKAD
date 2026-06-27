# CKAD v1.35 Lab Index — 2026 Edition

Hands-on labs for the **Certified Kubernetes Application Developer (CKAD)** exam. All 30 labs run on the free Killercoda Kubernetes Playground — no local installation required.

**Lab environment:** https://killercoda.com/playgrounds/scenario/kubernetes  
**Alternative:** https://labs.play-with-k8s.com

**First thing to run on every session:**
```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
source <(kubectl completion bash)
complete -o default -F __start_kubectl k
```

---

## Domain 1 — Application Design and Build (20%)

| Lab | Title | Key Skill |
|-----|-------|-----------|
| [Lab 01](lab-01-build-container-image.md) | Build a Container Image | Dockerfile, `docker build`, image layers |
| [Lab 02](lab-02-multistage-dockerfile.md) | Multi-Stage Dockerfile | `COPY --from=`, distroless, image size reduction |
| [Lab 03](lab-03-create-pods.md) | Create and Manage Pods | `kubectl run`, `--dry-run=client -o yaml`, `--restart=Never` |
| [Lab 04](lab-04-jobs.md) | Jobs | `completions`, `parallelism`, `backoffLimit`, `activeDeadlineSeconds` |
| [Lab 05](lab-05-cronjobs.md) | CronJobs | `concurrencyPolicy`, `timeZone`, manual trigger |
| [Lab 06](lab-06-sidecar-pod.md) | Sidecar / Multi-Container Pods | `emptyDir` sharing, native sidecar (k8s 1.29+) |
| [Lab 07](lab-07-init-containers.md) | Init Containers | Ordered startup, seed volumes, wait for services |
| [Lab 08](lab-08-volumes.md) | Volumes | `emptyDir`, `emptyDir.medium: Memory`, `hostPath` |

---

## Domain 2 — Application Deployment (20%)

| Lab | Title | Key Skill |
|-----|-------|-----------|
| [Lab 09](lab-09-deployments.md) | Deployments and ReplicaSets | Deployment → RS → Pod chain, `kubectl scale` |
| [Lab 10](lab-10-rolling-update.md) | Rolling Updates and Rollback | `maxSurge`, `maxUnavailable`, `kubectl rollout undo` |
| [Lab 11](lab-11-blue-green.md) | Blue/Green Deployment | Service selector flip, atomic cutover |
| [Lab 12](lab-12-canary.md) | Canary Deployment | Replica ratio traffic split, gradual promotion |
| [Lab 13](lab-13-helm.md) | Helm | `helm install`, `upgrade`, `rollback`, `--reuse-values` |
| [Lab 14](lab-14-kustomize.md) | Kustomize Overlays | `namePrefix`, `commonLabels`, `images`, `patches` |
| [Lab 15](lab-15-daemonset-statefulset.md) | DaemonSet and StatefulSet | Per-node scheduling, stable Pod DNS, ordered scale |

---

## Domain 3 — Application Observability and Maintenance (15%)

| Lab | Title | Key Skill |
|-----|-------|-----------|
| [Lab 16](lab-16-probes.md) | Liveness, Readiness, Startup Probes | `httpGet`, `tcpSocket`, `exec`, `startupProbe` |
| [Lab 17](lab-17-logging.md) | Container Logging | `kubectl logs -f`, `--previous`, `-c`, `-l selector` |
| [Lab 18](lab-18-metrics.md) | Metrics Server and kubectl top | `kubectl top node/pod --sort-by=cpu` |
| [Lab 19](lab-19-debug.md) | Debugging Pods and Events | `ImagePullBackOff`, `CrashLoopBackOff`, `OOMKilled`, `kubectl debug` |
| [Lab 20](lab-20-api-deprecations.md) | API Deprecations and kubectl explain | `kubectl api-resources`, `kubectl explain --recursive` |

---

## Domain 4 — Application Environment, Configuration, and Security (25%)

| Lab | Title | Key Skill |
|-----|-------|-----------|
| [Lab 21](lab-21-configmaps.md) | ConfigMaps | `--from-literal`, `envFrom`, volume mount, live update |
| [Lab 22](lab-22-secrets.md) | Secrets | `generic`, `tls`, `docker-registry`, `defaultMode: 0400` |
| [Lab 23](lab-23-securitycontext.md) | SecurityContext | `runAsNonRoot`, `readOnlyRootFilesystem`, `capabilities.drop` |
| [Lab 24](lab-24-serviceaccounts.md) | ServiceAccounts | `kubectl create token`, `automountServiceAccountToken: false` |
| [Lab 25](lab-25-rbac.md) | RBAC | Role, ClusterRole, `kubectl auth can-i --as=` |
| [Lab 26](lab-26-quota-limitrange.md) | ResourceQuota and LimitRange | Aggregate namespace quotas, per-container defaults |

---

## Domain 5 — Services and Networking (20%)

| Lab | Title | Key Skill |
|-----|-------|-----------|
| [Lab 27](lab-27-services.md) | Services | ClusterIP, NodePort, LoadBalancer, endpoint debugging |
| [Lab 28](lab-28-service-dns.md) | Service DNS | FQDN, cross-namespace, `ndots:5`, headless Service |
| [Lab 29](lab-29-ingress-tls.md) | Ingress with TLS | `networking.k8s.io/v1`, TLS Secret, path routing |
| [Lab 30](lab-30-networkpolicy.md) | NetworkPolicy | Default-deny, `podSelector`, `namespaceSelector`, egress DNS |

---

## Exam Quick Reference

### API Versions (Kubernetes v1.35)
| Resource | apiVersion |
|----------|------------|
| Pod, Service, ConfigMap, Secret, Namespace, ServiceAccount, ResourceQuota, LimitRange | `v1` |
| Deployment, StatefulSet, DaemonSet, ReplicaSet | `apps/v1` |
| Job, CronJob | `batch/v1` |
| Ingress, NetworkPolicy | `networking.k8s.io/v1` |
| Role, RoleBinding, ClusterRole, ClusterRoleBinding | `rbac.authorization.k8s.io/v1` |
| HorizontalPodAutoscaler | `autoscaling/v2` |
| PodDisruptionBudget | `policy/v1` |

### Most-Used kubectl Commands
```bash
# Generate YAML scaffold
kubectl run <name> --image=<img> --dry-run=client -o yaml > pod.yaml
kubectl create deployment <name> --image=<img> --dry-run=client -o yaml > deploy.yaml

# Apply and delete
kubectl apply -f file.yaml
kubectl delete pod <name> --force --grace-period=0

# Inspect
kubectl describe pod <name>
kubectl get events --sort-by=.lastTimestamp
kubectl logs <pod> -c <container> --previous

# RBAC validation
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>

# Rollout
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout history deployment/<name>
```

### Exam-Allowed Documentation
- https://kubernetes.io/docs/
- https://helm.sh/docs/
- https://kubernetes.io/docs/reference/kubectl/cheatsheet/
