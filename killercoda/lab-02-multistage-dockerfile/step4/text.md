# Step 4: Compare image sizes

```bash
docker images | grep demo
```

Expected output:
```
demo   single   ...   ~800MB
demo   multi    ...   ~8MB
```

The `distroless` runtime has no shell, no package manager, no attack surface.

---
