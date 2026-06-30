# Lab 20 — API Deprecations and kubectl explain

The Kubernetes API evolves across releases — old API versions are deprecated and eventually removed. CKAD 2026 tests `kubectl explain`, `kubectl api-resources`, and `kubectl api-versions`. You must be able to find the correct `apiVersion` for any resource on exam day using only kubectl.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — List every resource and its API group

```bash
k api-resources | head -20
k api-resources --namespaced=true | head -10
k api-resources --api-group=apps
k api-resources --api-group=batch
```

The `APIVERSION` column tells you exactly what to write in `apiVersion:` in your YAML.

---

## Step 3 — List all API versions served by the cluster

```bash
k api-versions | sort
```

Use this to confirm which versions are available before writing a manifest.

---

## Step 4 — Explore a resource schema with explain

```bash
k explain deployment
k explain deployment.spec
k explain deployment.spec.strategy.rollingUpdate
k explain pod.spec.containers.resources --recursive | head -30
```

`--recursive` prints the full field tree — use it when you forget the exact path to a nested field during the exam.

---

## Step 5 — Detect a deprecated API

```bash
cat > old.yaml <<'EOF'
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: legacy
spec: {}
EOF
k apply -f old.yaml --dry-run=client 2>&1 || true
```

`extensions/v1beta1` Ingress was removed in Kubernetes 1.22. The current stable version is `networking.k8s.io/v1`.

---

## Step 6 — Look up the correct API version

```bash
k explain ingress --api-version=networking.k8s.io/v1 | head -10
k api-resources | grep -i ingress
```

This is the exam technique: when unsure of the `apiVersion`, run `api-resources` and read the `APIVERSION` column.

---

## Step 7 — Stable API version reference (Kubernetes v1.35)

| Resource | apiVersion |
|----------|------------|
| Pod, Service, ConfigMap, Secret, Namespace, ServiceAccount | `v1` |
| Deployment, StatefulSet, DaemonSet, ReplicaSet | `apps/v1` |
| Job, CronJob | `batch/v1` |
| Ingress, NetworkPolicy | `networking.k8s.io/v1` |
| Role, RoleBinding, ClusterRole, ClusterRoleBinding | `rbac.authorization.k8s.io/v1` |
| HorizontalPodAutoscaler | `autoscaling/v2` |
| PodDisruptionBudget | `policy/v1` |
| ResourceQuota, LimitRange | `v1` |

---

## Step 8 — Clean up

```bash
rm -f old.yaml
```

---

## Free online tools

- **API deprecation guide**: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
- **kubectl explain reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/
- **Kubernetes API reference (v1.35)**: https://kubernetes.io/docs/reference/kubernetes-api/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl api-resources` shows the correct `apiVersion` for every resource.
- `kubectl explain <resource>.<field>` is the exam-legal way to look up field names.
- `--recursive` on `explain` dumps the full schema tree — saves time on nested fields.
- Memorise the v1.35 stable API versions table above; deprecations are frequently tested.
