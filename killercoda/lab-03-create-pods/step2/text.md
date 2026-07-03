# Step 2: Create a Pod imperatively

```bash
k run web --image=nginx:1.25 --port=80
k get pod web -o wide
```

`kubectl run` is the fastest path to a running Pod. `-o wide` shows the node and Pod IP.

---
