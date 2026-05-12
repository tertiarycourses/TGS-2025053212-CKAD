# Lab 26 — ResourceQuota and LimitRange

`ResourceQuota` caps the **total** resources used in a namespace. `LimitRange` sets **per-Pod / per-container** defaults and maximums. In this lab you will apply both and watch them refuse over-budget workloads.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Set up a dedicated namespace

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

---

## Step 3 — Apply a LimitRange (defaults + maximums)

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
    default:           # default limit
      cpu: 200m
      memory: 256Mi
    defaultRequest:    # default request
      cpu: 100m
      memory: 128Mi
    max:
      cpu: 500m
      memory: 512Mi
EOF
k apply -f limits.yaml
```

---

## Step 4 — Launch a Pod with no resource block

```bash
k run a --image=nginx:1.25 -n team-a
k get pod a -n team-a -o jsonpath='{.spec.containers[0].resources}'; echo
```

LimitRange auto-populated requests and limits.

---

## Step 5 — Try to violate the LimitRange

```bash
k run big --image=nginx:1.25 -n team-a \
  --overrides='{"spec":{"containers":[{"name":"big","image":"nginx:1.25","resources":{"limits":{"cpu":"1","memory":"1Gi"}}}]}}' \
  2>&1 | head -3
```

Rejected with `maximum cpu usage per Container is 500m`.

---

## Step 6 — Try to exceed the ResourceQuota

```bash
for i in 1 2 3 4; do k run quota-$i --image=nginx:1.25 -n team-a; done
k run quota-5 --image=nginx:1.25 -n team-a 2>&1 | head -3   # should fail: 6th pod
```

`pods: "5"` quota refuses the sixth Pod.

---

## Step 7 — Clean up

```bash
k delete namespace team-a
```

---

## What you learned
- ResourceQuota caps **aggregate** namespace usage.
- LimitRange enforces **per-container** defaults and maximums.
- The two work together to keep noisy tenants under control.
