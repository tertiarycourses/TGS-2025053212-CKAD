# Step 2: Create Services in two namespaces

```bash
k create ns app
k create ns probe

k -n app create deployment web --image=nginx:1.25 --replicas=2
k -n app expose deployment web --port=80
```

---
