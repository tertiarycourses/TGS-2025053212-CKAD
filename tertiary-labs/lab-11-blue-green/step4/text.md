# Step 4: Smoke-test green directly before cutover

```bash
GREEN_POD=$(k get pod -l version=green -o jsonpath='{.items[0].metadata.name}')
k exec $GREEN_POD -- curl -sI localhost:80 | head -2
```

Validate green is healthy before switching traffic.

---
