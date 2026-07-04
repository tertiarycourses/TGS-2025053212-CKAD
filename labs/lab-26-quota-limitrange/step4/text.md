# Step 4: Pod with no resource block gets defaults injected

```bash
k run a --image=nginx:1.25 -n team-a
k get pod a -n team-a -o jsonpath='{.spec.containers[0].resources}'; echo
```

LimitRange automatically populated `requests` and `limits` — the Pod is accepted without you specifying any resources.

---
