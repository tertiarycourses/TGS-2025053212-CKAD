# Step 3: Read logs from each container separately

```bash
k logs app-with-sidecar -c app | head -5
k logs app-with-sidecar -c log-shipper | head -5
k logs app-with-sidecar --all-containers=true --prefix=true | head -10
```

`-c <name>` selects the container. On exam: when a Pod has multiple containers, always specify `-c`.

---
