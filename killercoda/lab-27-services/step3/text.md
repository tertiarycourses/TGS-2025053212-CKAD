# Step 3: ClusterIP Service (in-cluster only)

```bash
k expose deployment web --port=80 --target-port=80 --name=web-cip
k get svc web-cip
k describe svc web-cip | grep -E "IP:|Endpoints:"
```

Test from inside the cluster:

```bash
k run probe --image=busybox --restart=Never -it --rm -- wget -qO- web-cip
```

A ClusterIP is reachable only by other Pods in the cluster — not from outside.

---
