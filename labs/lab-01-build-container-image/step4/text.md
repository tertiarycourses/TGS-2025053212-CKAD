# Step 4: Build and tag the image

```bash
docker build -t ckad/hello:1.0 .
```

The `-t` flag sets the tag (`name:version`). The trailing `.` is the build context — the directory whose files `COPY` can access. Expect 30–60 seconds on first run while the base image downloads.

---
