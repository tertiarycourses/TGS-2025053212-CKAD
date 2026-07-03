# Step 3: Generate a Pod manifest without creating it

```bash
k run web2 --image=nginx:1.25 --port=80 $do > web2.yaml
cat web2.yaml
```

`$do` expands to `--dry-run=client -o yaml`. Redirect to a file, edit, then apply — the standard CKAD workflow.

---
