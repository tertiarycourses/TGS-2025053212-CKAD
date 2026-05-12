# Free Tools Reference — CKAD v1.35 Labs

Every tool listed here is **100% free** (open-source, freeware, or free tier with no time limit).

Two categories:

1. **Inside Killercoda** — pre-installed in the throw-away Kubernetes VM, or installed during a lab. Nothing touches your own machine.
2. **External / Standalone** — downloaded onto your own PC/laptop, or used in a browser. Useful when you're offline, on a school PC, or want a GUI.

Killercoda Kubernetes playground (free, no signup): https://killercoda.com/playgrounds/scenario/kubernetes

---

## Section A — Tools inside the Killercoda Kubernetes VM

### A1. Pre-installed (already in the playground)
| Tool | Purpose | Used in Lab |
|------|---------|-------------|
| `kubectl` | Kubernetes CLI | every lab |
| `docker` | Container build & run | 1, 2 |
| `kubeadm` / `kubelet` | Single-node cluster bootstrap | already running |
| Calico CNI | Pod networking + NetworkPolicy enforcement | 30 |
| `containerd` | Container runtime under kubelet | implicit |
| `crictl` | CRI debug tool | 19 |
| `curl`, `wget`, `jq`, `vim`, `nano` | General CLI utilities | many |

### A2. Installed during a specific lab
| Tool | Install | Purpose | Lab |
|------|---------|---------|-----|
| Helm 3 | `curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \| bash` | Package manager for Kubernetes | 13 |
| metrics-server | `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml` | Provides CPU/memory metrics for `kubectl top` | 18 |
| ingress-nginx | `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml` | NGINX Ingress controller | 29 |
| `openssl` | pre-installed | Generate self-signed TLS cert | 29 |
| `kustomize` | Built into `kubectl -k` | Manifest overlays | 14 |

### A3. Useful imperative kubectl shortcuts (exam-day)
| Alias / var | Definition | Why |
|-------------|-----------|-----|
| `alias k=kubectl` | shorter | typing speed |
| `export do="--dry-run=client -o yaml"` | YAML template | scaffold manifests instantly |
| `export now="--force --grace-period 0"` | force-delete | unstuck pods |
| `source <(kubectl completion bash)` | tab-complete | autocomplete resources |
| `complete -F __start_kubectl k` | apply completion to `k` | autocomplete for alias |

---

## Section B — External / Standalone free tools

### B1. Local Kubernetes clusters (alternative to Killercoda)
| Tool | Type | Link |
|------|------|------|
| Minikube | macOS / Linux / Windows | https://minikube.sigs.k8s.io |
| kind (Kubernetes-in-Docker) | All OSes | https://kind.sigs.k8s.io |
| k3s | Lightweight Linux distro | https://k3s.io |
| k3d (k3s in Docker) | All OSes | https://k3d.io |
| Docker Desktop Kubernetes | Bundled toggle | https://www.docker.com/products/docker-desktop |
| MicroK8s | Snap-based, Ubuntu | https://microk8s.io |
| Rancher Desktop | macOS / Windows / Linux | https://rancherdesktop.io |

### B2. Browser sandboxes
| Service | What you get | Link |
|---------|--------------|------|
| **Killercoda Kubernetes Playground** ⭐ | Root + kubectl on a live cluster | https://killercoda.com/playgrounds/scenario/kubernetes |
| Killer.sh CKAD simulator | Two free sessions with exam purchase | https://killer.sh/ckad |
| Play with Kubernetes | 4-hour cluster in browser | https://labs.play-with-k8s.com |
| KodeKloud Playgrounds | Free tier | https://kodekloud.com/playgrounds |
| Instruqt CKAD tracks | Free hands-on tracks | https://instruqt.com |

### B3. Container build / registry (Lab 1, 2)
| Tool | Type | Link |
|------|------|------|
| Docker Engine | All OSes | https://docs.docker.com/engine |
| Podman | Daemonless alternative | https://podman.io |
| BuildKit / buildx | Multi-platform builds | https://github.com/moby/buildkit |
| Skopeo | Copy images between registries | https://github.com/containers/skopeo |
| Dive | Inspect image layers | https://github.com/wagoodman/dive |
| Hadolint | Dockerfile linter | https://github.com/hadolint/hadolint |
| Docker Hub (free tier) | Public image registry | https://hub.docker.com |
| GitHub Container Registry | Free for public | https://ghcr.io |
| Quay.io (free for public) | Public registry | https://quay.io |

### B4. kubectl tooling (every lab)
| Tool | Type | Link |
|------|------|------|
| kubectl | All OSes | https://kubernetes.io/docs/tasks/tools/ |
| kubectx + kubens | Context / namespace switcher | https://github.com/ahmetb/kubectx |
| krew | kubectl plugin manager | https://krew.sigs.k8s.io |
| kube-ps1 | Show context in prompt | https://github.com/jonmosco/kube-ps1 |
| stern | Multi-pod log tail | https://github.com/stern/stern |
| k9s | Terminal UI for clusters | https://k9scli.io |
| kubeshark | API-aware traffic viewer | https://www.kubeshark.co |

### B5. Package and manifest management (Lab 13, 14)
| Tool | Type | Link |
|------|------|------|
| Helm 3 | All OSes | https://helm.sh |
| Kustomize | All OSes (also `kubectl -k`) | https://kustomize.io |
| Helmfile | Declarative Helm | https://helmfile.readthedocs.io |
| ArtifactHub | Search public Helm charts | https://artifacthub.io |

### B6. Probes / health (Lab 16)
| Tool | Type | Link |
|------|------|------|
| `curl` | CLI | bundled |
| `wget` | CLI | bundled |
| `grpc_health_probe` | gRPC liveness probe | https://github.com/grpc-ecosystem/grpc-health-probe |

### B7. Logging / observability (Lab 17, 18, 19)
| Tool | Type | Link |
|------|------|------|
| metrics-server | Cluster add-on | https://github.com/kubernetes-sigs/metrics-server |
| `kubectl logs` / `kubectl events` | Built-in | — |
| stern | Multi-pod log tail | https://github.com/stern/stern |
| kail | kubectl log forwarder | https://github.com/boz/kail |
| Loki + Grafana | Self-hosted logs | https://grafana.com/oss/loki/ |
| Prometheus + Grafana | Self-hosted metrics | https://prometheus.io |
| Lens IDE (free) | Cluster GUI | https://k8slens.dev |
| Octant (archived but works) | Web cluster GUI | https://github.com/vmware-archive/octant |

### B8. Debugging (Lab 19)
| Tool | Type | Link |
|------|------|------|
| `kubectl debug` | Ephemeral debug containers | built-in |
| `kubectl describe` / `kubectl events` | Built-in | — |
| crictl | CRI debug tool | https://github.com/kubernetes-sigs/cri-tools |
| nicolaka/netshoot | Network debug image | https://github.com/nicolaka/netshoot |
| busybox / alpine | Disposable debug shells | Docker Hub |

### B9. Security / RBAC (Lab 22, 23, 24, 25)
| Tool | Type | Link |
|------|------|------|
| `kubectl auth can-i` | Built-in RBAC simulator | — |
| `rakkess` | Resource access matrix | https://github.com/corneliusweig/rakkess |
| `kubectl-who-can` | Reverse RBAC lookup | https://github.com/aquasecurity/kubectl-who-can |
| `kube-bench` | CIS benchmark scanner | https://github.com/aquasecurity/kube-bench |
| `trivy` | Image + cluster vulnerability scanner | https://github.com/aquasecurity/trivy |
| Falco | Runtime security | https://falco.org |
| OPA Gatekeeper | Policy controller | https://open-policy-agent.github.io/gatekeeper/ |
| Kyverno | Policy controller | https://kyverno.io |
| `kubeseal` (Sealed Secrets) | Encrypt Secrets into Git | https://sealed-secrets.netlify.app |
| `sops` | Secret encryption | https://github.com/getsops/sops |

### B10. Networking & Ingress (Lab 27, 28, 29, 30)
| Tool | Type | Link |
|------|------|------|
| ingress-nginx | Ingress controller | https://kubernetes.github.io/ingress-nginx/ |
| Traefik | Ingress controller | https://traefik.io |
| HAProxy Ingress | Ingress controller | https://haproxy-ingress.github.io |
| MetalLB | LoadBalancer for bare-metal | https://metallb.universe.tf |
| Cilium | CNI + NetworkPolicy + L7 | https://cilium.io |
| Calico | CNI + NetworkPolicy | https://www.tigera.io/project-calico/ |
| `kubectl port-forward` | Built-in | — |

### B11. YAML / manifest authoring
| Tool | Type | Link |
|------|------|------|
| VS Code + Kubernetes extension | Cross-platform | https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools |
| YAMLLint | Web / CLI | https://www.yamllint.com |
| `kubeval` | Manifest schema validation | https://www.kubeval.com |
| `kubeconform` | Faster kubeval replacement | https://github.com/yannh/kubeconform |
| `kube-score` | Best-practice linter | https://github.com/zegl/kube-score |
| Datree | Policy-as-code checks | https://www.datree.io |

### B12. Practice & study (allowed during real CKAD exam)
| Tool | Type | Link |
|------|------|------|
| Kubernetes docs | Web | https://kubernetes.io/docs |
| Helm docs | Web | https://helm.sh/docs |
| kubectl cheatsheet | Web | https://kubernetes.io/docs/reference/kubectl/cheatsheet/ |
| CKAD curriculum v1.35 PDF | PDF | https://github.com/cncf/curriculum |
| CKAD exam prep repo (this course's answer key) | GitHub | https://github.com/ChathurangaVKD/ckad-exam-prep |
| Killer.sh CKAD simulator | Web | https://killer.sh/ckad |

---

## Lab → Primary Tool Quick Map

| Lab | Headline tool(s) |
|-----|------------------|
| 1 | `docker build`, `docker run` |
| 2 | `docker build` multi-stage |
| 3 | `kubectl run`, `kubectl get pod` |
| 4 | `kubectl create job`, `Job` resource |
| 5 | `kubectl create cronjob`, `CronJob` resource |
| 6 | Pod with multiple `containers:` |
| 7 | `initContainers:` |
| 8 | `emptyDir`, `hostPath` volumes |
| 9 | `kubectl create deployment` |
| 10 | `kubectl rollout` |
| 11 | Two Deployments + Service selector swap |
| 12 | Weighted Deployments + shared Service |
| 13 | `helm install`, `helm upgrade` |
| 14 | `kubectl apply -k`, overlays |
| 15 | `DaemonSet`, `StatefulSet` |
| 16 | `livenessProbe`, `readinessProbe`, `startupProbe` |
| 17 | `kubectl logs`, multi-container `-c` |
| 18 | `metrics-server`, `kubectl top` |
| 19 | `kubectl describe`, `kubectl events`, `kubectl debug` |
| 20 | `kubectl explain`, `kubectl api-resources` |
| 21 | `kubectl create configmap`, `envFrom`, volume mount |
| 22 | `kubectl create secret`, `envFrom`, volume mount |
| 23 | `securityContext`, `runAsUser`, `runAsNonRoot` |
| 24 | `ServiceAccount`, automount token |
| 25 | `Role`, `RoleBinding`, `kubectl auth can-i` |
| 26 | `ResourceQuota`, `LimitRange` |
| 27 | `Service` ClusterIP / NodePort / LoadBalancer |
| 28 | CoreDNS, FQDN `svc.ns.svc.cluster.local` |
| 29 | `Ingress` with `tls:` block |
| 30 | `NetworkPolicy` ingress / egress |

---

All tools above are free of charge. The Killercoda Kubernetes VM is also free and disposable, so you can run every lab without spending or installing anything on your own machine.
