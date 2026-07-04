# Step 7: Request a short-lived ad-hoc token

```bash
TOKEN=$(k create token app-sa --duration=1h)
echo $TOKEN | cut -c1-60
echo "... (truncated)"
```

`kubectl create token` replaces the old long-lived Secret-backed tokens removed in Kubernetes 1.24+.

---
