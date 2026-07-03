# Step 2: One-shot Job (imperative)

```bash
k create job hello --image=busybox -- echo "hello CKAD 2026"
k get jobs,pods -l job-name=hello
k logs -l job-name=hello
```

A Job creates a Pod, waits for it to exit 0, and marks the Job `Complete`. The Pod is retained for log inspection.

---
