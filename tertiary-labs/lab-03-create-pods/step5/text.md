# Step 5: Inspect a running Pod

```bash
k describe pod web
k get pod web -o jsonpath='{.status.podIP}'; echo
```

`describe` shows Events, image pulls, volume mounts, and probe status — the primary debugging tool. `jsonpath` extracts single fields for scripting.

---
