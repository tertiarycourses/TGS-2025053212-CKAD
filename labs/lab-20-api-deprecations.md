# Lab 20 — API Deprecations and kubectl explain

The Kubernetes API surface changes between releases. CKAD candidates must know how to look up the current API for any resource and detect deprecated fields. In this lab you will use `kubectl explain`, `kubectl api-resources`, and `kubectl api-versions`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — List every resource and its API group/version

```bash
alias k=kubectl
k api-resources | head
k api-resources --namespaced=true | head
k api-resources --api-group=apps
```

The `APIVERSION` column tells you exactly what to put in `apiVersion:` in your YAML.

---

## Step 2 — List API versions served by this cluster

```bash
k api-versions | sort
```

---

## Step 3 — Explore a resource schema with `explain`

```bash
k explain deployment
k explain deployment.spec
k explain deployment.spec.strategy.rollingUpdate
k explain pod.spec.containers.resources --recursive | head -30
```

`--recursive` is great when you forget the exact path for a deeply nested field.

---

## Step 4 — Detect deprecated APIs in a YAML file

```bash
cat > old.yaml <<'EOF'
apiVersion: extensions/v1beta1
kind: Ingress
metadata: { name: legacy }
spec: {}
EOF
k apply -f old.yaml --dry-run=client 2>&1 || true
```

Older `extensions/v1beta1` Ingress was removed; the current stable version is `networking.k8s.io/v1`.

---

## Step 5 — Look up the current stable API

```bash
k explain ingress --api-version=networking.k8s.io/v1 | head
```

Use this technique to confirm the right `apiVersion` for any resource on exam day.

---

## Step 6 — Quick reference: stable v1.35 API versions

| Resource | apiVersion |
|----------|------------|
| Pod, Service, ConfigMap, Secret, Namespace | `v1` |
| Deployment, StatefulSet, DaemonSet, ReplicaSet | `apps/v1` |
| Job, CronJob | `batch/v1` |
| Ingress, NetworkPolicy | `networking.k8s.io/v1` |
| Role, RoleBinding, ClusterRole, ClusterRoleBinding | `rbac.authorization.k8s.io/v1` |
| HorizontalPodAutoscaler | `autoscaling/v2` |
| ServiceAccount | `v1` |

---

## Step 7 — Clean up

```bash
rm -f old.yaml
```

---

## What you learned
- `kubectl api-resources`, `kubectl api-versions`, `kubectl explain`.
- How to confirm an `apiVersion` for any resource.
- How to detect deprecated APIs before applying YAML.
