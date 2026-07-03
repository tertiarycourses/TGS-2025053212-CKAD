# Step 4: Explore a resource schema with explain

```bash
k explain deployment
k explain deployment.spec
k explain deployment.spec.strategy.rollingUpdate
k explain pod.spec.containers.resources --recursive | head -30
```

`--recursive` prints the full field tree — use it when you forget the exact path to a nested field during the exam.

---
