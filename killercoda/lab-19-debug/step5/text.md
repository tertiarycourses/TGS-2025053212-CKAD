# Step 5: Cluster-wide event stream

```bash
k get events -A --sort-by=.lastTimestamp | tail -20
k get events --field-selector type=Warning
```

`get events` is the fastest way to see what the cluster has been doing — more concise than `describe` across many Pods.

---
