# Step 6: Inspect the image layers

```bash
docker images ckad/hello
docker history ckad/hello:1.0
```

`docker history` prints one row per instruction. Use it to prove each Dockerfile line becomes a distinct layer.

---
