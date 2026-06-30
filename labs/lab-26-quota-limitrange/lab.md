# Lab 26 — ResourceQuota and LimitRange

`ResourceQuota` caps the **total** resources used across an entire namespace. `LimitRange` enforces **per-container** defaults and maximums. CKAD 2026 tests both objects — you must write the YAML, apply them, and understand the error messages when a workload is rejected.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25` image (pulled automatically)

---

## Step 1 — Set exam aliases and create a test namespace

```bash
alias k=kubectl
k create namespace team-a
```

---

## Step 2 — Apply a ResourceQuota

```bash
cat > quota.yaml <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    pods: "5"
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
EOF
k apply -f quota.yaml
k describe quota team-a-quota -n team-a
```

`hard` sets the maximum totals. Once any value is reached, new Pods in the namespace are rejected.

---

## Step 3 — Apply a LimitRange (defaults and maximums)

```bash
cat > limits.yaml <<'EOF'
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:
      cpu: 200m
      memory: 256Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    max:
      cpu: 500m
      memory: 512Mi
EOF
k apply -f limits.yaml
```

`default` = limit injected when the container has none. `defaultRequest` = request injected when missing. `max` = hard ceiling per container.

---

## Step 4 — Pod with no resource block gets defaults injected

```bash
k run a --image=nginx:1.25 -n team-a
k get pod a -n team-a -o jsonpath='{.spec.containers[0].resources}'; echo
```

LimitRange automatically populated `requests` and `limits` — the Pod is accepted without you specifying any resources.

---

## Step 5 — Violate the LimitRange maximum

```bash
k run big --image=nginx:1.25 -n team-a \
  --overrides='{"spec":{"containers":[{"name":"big","image":"nginx:1.25","resources":{"limits":{"cpu":"1","memory":"1Gi"}}}]}}' \
  2>&1 | head -5
```

Rejected: `maximum cpu usage per Container is 500m`. The LimitRange enforced the `max` ceiling.

---

## Step 6 — Exceed the ResourceQuota

```bash
for i in 1 2 3 4; do k run quota-$i --image=nginx:1.25 -n team-a; done
k run quota-5 --image=nginx:1.25 -n team-a 2>&1 | head -3
```

The 6th Pod (pods quota is `5`) is rejected: `exceeded quota: team-a-quota`.

---

## Step 7 — Inspect quota usage

```bash
k describe quota team-a-quota -n team-a
```

The `Used` column shows current consumption against `Hard` limits.

---

## Step 8 — Clean up

```bash
k delete namespace team-a
```

---

## Free online tools

- **ResourceQuota docs**: https://kubernetes.io/docs/concepts/policy/resource-quotas/
- **LimitRange docs**: https://kubernetes.io/docs/concepts/policy/limit-range/
- **Resource units reference**: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ResourceQuota` limits **aggregate** usage in a namespace; exceeding it rejects new Pods.
- `LimitRange` enforces **per-container** minimums, maximums, and defaults.
- Without a LimitRange, Pods with no resource block cannot be created in a quota-enforced namespace.
- `kubectl describe quota` shows current `Used` vs `Hard` — the primary troubleshooting tool.
