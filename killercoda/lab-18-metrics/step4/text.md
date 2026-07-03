# Step 4: Top Pods, sorted by CPU and memory

```bash
k top pod
k top pod --sort-by=cpu
k top pod --sort-by=memory
k top pod -A --sort-by=cpu | head -10
```

`cpu-burner` should appear at the top of the CPU sort. `-A` covers all namespaces.

---
