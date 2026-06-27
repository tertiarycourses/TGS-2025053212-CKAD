# Free Tools Reference — CKAD v1.35 (2026) Labs

Every tool listed here is **100% free**. No credit card, no time limit.

Two categories:
1. **Inside Killercoda** — pre-installed in the disposable Kubernetes VM.
2. **External / Browser** — used outside the VM for reference, practice, or validation.

Primary lab environment (free, no signup required):
https://killercoda.com/playgrounds/scenario/kubernetes

Alternative environments if Killercoda is unavailable:
- **Play with Kubernetes**: https://labs.play-with-k8s.com
- **Play with Docker**: https://labs.play-with-docker.com
- **GitHub Codespaces** (free quota): https://github.com/features/codespaces

---

## Section A — Tools Pre-Installed in Killercoda Kubernetes VM

### A1. Core Kubernetes Tools
| Tool | Purpose | Labs |
|------|---------|------|
| `kubectl` | All Kubernetes operations | All labs |
| `kubectl kustomize` | Kustomize rendering (built into kubectl) | 14 |
| `docker` | Build and run container images | 1, 2 |
| `containerd` / `crictl` | Container runtime; ephemeral container debugging | 19 |
| `helm` | Install via one-line script (Lab 13 Step 1) | 13 |

### A2. System and Network Tools
| Tool | Install | Purpose | Labs |
|------|---------|---------|------|
| `curl` | pre-installed | Test HTTP Services and Ingress | 1, 5, 10, 27, 29 |
| `wget` | pre-installed | Test Services from inside Pods | 11, 12, 27, 30 |
| `nslookup` / `dig` | pre-installed | DNS resolution testing | 7, 15, 28 |
| `openssl` | pre-installed | Generate self-signed TLS certs | 22, 29 |
| `bash` / `sh` | pre-installed | Scripting and heredoc manifests | All labs |

### A3. Text Manipulation
| Tool | Purpose | Labs |
|------|---------|------|
| `sed` | In-place YAML edits | 3, 10 |
| `grep` | Filter `describe` and `get` output | All labs |
| `base64` | Encode/decode Secret values | 22 |
| `jq` | JSON parsing (available via `apt install jq`) | 24 |

---

## Section B — External / Browser Tools

### B1. Exam Practice
| Tool | Type | Purpose |
|------|------|---------|
| **killer.sh** ⭐ | Web (paid add-on) | Official CKAD mock exam — closest to real exam environment |
| **Killercoda CKAD scenarios** | Web (free) | Curated CKAD practice scenarios |
| **KodeKloud CKAD labs** | Web (free tier) | Browser-based Kubernetes practice |

Links:
- killer.sh: https://killer.sh
- Killercoda CKAD: https://killercoda.com/killer-shell-ckad
- KodeKloud: https://kodekloud.com

### B2. Official Documentation (Allowed During CKAD Exam)
| Resource | URL |
|----------|-----|
| **Kubernetes docs** ⭐ | https://kubernetes.io/docs/ |
| **kubectl cheat sheet** ⭐ | https://kubernetes.io/docs/reference/kubectl/cheatsheet/ |
| **API reference (v1.35)** | https://kubernetes.io/docs/reference/kubernetes-api/ |
| **kubectl generated reference** | https://kubernetes.io/docs/reference/kubectl/generated/ |
| **Helm docs** | https://helm.sh/docs/ |

### B3. Image Registries
| Registry | Purpose |
|----------|---------|
| **DockerHub** — https://hub.docker.com | Find and inspect base images |
| **Artifact Hub** — https://artifacthub.io | Search Helm charts |
| **Google Distroless** — https://github.com/GoogleContainerTools/distroless | Minimal runtime base images |
| **Bitnami Charts** — https://github.com/bitnami/charts | Production Helm charts |

### B4. Networking and Policy Tools
| Tool | Type | Purpose |
|------|------|---------|
| **NetworkPolicy Editor** | Web | Visual NetworkPolicy builder | 
| **SSL Labs** | Web | Test TLS configuration |
| **CoreDNS docs** | Web | DNS configuration reference |

Links:
- NetworkPolicy Editor: https://editor.networkpolicy.io
- SSL Labs: https://www.ssllabs.com/ssltest
- CoreDNS: https://coredns.io/docs/

### B5. YAML and Kubernetes Utilities
| Tool | Type | Purpose |
|------|------|---------|
| **YAML Lint** | Web | Validate YAML syntax before applying |
| **Lens Desktop** | App | Visual Kubernetes cluster explorer |
| **k9s** | CLI | Terminal-based cluster UI |
| **crontab.guru** | Web | Validate cron schedule expressions |

Links:
- YAML Lint: https://www.yamllint.com
- Lens: https://k8slens.dev
- k9s: https://k9scli.io
- crontab.guru: https://crontab.guru

---

## Lab → Primary Tool Quick Map

| Lab | Topic | Key Commands |
|-----|-------|-------------|
| 1 | Container images | `docker build`, `docker run`, `docker history` |
| 2 | Multi-stage builds | `docker build -f`, `COPY --from=` |
| 3 | Pods | `kubectl run`, `kubectl apply`, `--dry-run=client -o yaml` |
| 4 | Jobs | `kubectl create job`, `completions`, `parallelism` |
| 5 | CronJobs | `kubectl create cronjob`, `kubectl create job --from=cronjob/` |
| 6 | Sidecar / Multi-container | `kubectl logs -c`, `kubectl exec -c` |
| 7 | Init containers | `kubectl get pod` (watch Init:N/M) |
| 8 | Volumes | `emptyDir`, `hostPath`, `volumeMounts` |
| 9 | Deployments | `kubectl create deployment`, `kubectl scale`, `kubectl set env` |
| 10 | Rolling updates | `kubectl set image`, `kubectl rollout`, `kubectl rollout undo` |
| 11 | Blue/Green | `kubectl patch service` (selector flip) |
| 12 | Canary | `kubectl scale` (replica ratio) |
| 13 | Helm | `helm install`, `helm upgrade`, `helm rollback` |
| 14 | Kustomize | `kubectl apply -k`, `kubectl kustomize` |
| 15 | DaemonSet / StatefulSet | `kubectl rollout status sts/` |
| 16 | Probes | `livenessProbe`, `readinessProbe`, `startupProbe` |
| 17 | Logging | `kubectl logs -f`, `--previous`, `--all-containers` |
| 18 | Metrics | `kubectl top node`, `kubectl top pod --sort-by=cpu` |
| 19 | Debugging | `kubectl describe`, `kubectl get events`, `kubectl debug` |
| 20 | API deprecations | `kubectl api-resources`, `kubectl explain` |
| 21 | ConfigMaps | `configMapKeyRef`, `envFrom`, volume mount |
| 22 | Secrets | `secretRef`, `defaultMode: 0400`, `base64 -d` |
| 23 | SecurityContext | `runAsUser`, `readOnlyRootFilesystem`, `capabilities.drop` |
| 24 | ServiceAccounts | `kubectl create token`, `automountServiceAccountToken` |
| 25 | RBAC | `kubectl auth can-i --as=`, Role, ClusterRole |
| 26 | Quota / LimitRange | `kubectl describe quota`, `hard:`, `defaultRequest:` |
| 27 | Services | `kubectl expose`, ClusterIP, NodePort, LoadBalancer |
| 28 | Service DNS | FQDN format, `ndots:5`, headless Service |
| 29 | Ingress + TLS | `networking.k8s.io/v1`, `pathType: Prefix`, TLS Secret |
| 30 | NetworkPolicy | default-deny, `podSelector`, `namespaceSelector` |

---

## Exam Day Setup (Run This First)

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
source <(kubectl completion bash)
complete -o default -F __start_kubectl k
```

These four lines save significant time in the real exam. Set them in the first 30 seconds.
