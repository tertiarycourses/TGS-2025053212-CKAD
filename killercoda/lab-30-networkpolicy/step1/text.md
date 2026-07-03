# Step 1: Set exam aliases and create workloads

```bash
alias k=kubectl
k create ns secured
k -n secured create deployment backend --image=hashicorp/http-echo -- -text=backend-ok
k -n secured expose deployment backend --port=5678
k -n secured run client-ok  --image=busybox --labels=role=allowed \
  --command -- sh -c 'sleep 3600'
k -n secured run client-bad --image=busybox --labels=role=blocked \
  --command -- sh -c 'sleep 3600'
k -n secured wait --for=condition=Ready pod --all --timeout=60s
```

Confirm both clients can reach the backend before any policy is applied:

```bash
for p in client-ok client-bad; do
  echo "--- $p ---"
  k -n secured exec $p -- wget -qO- --timeout=3 backend:5678
done
```

---
