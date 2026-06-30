# Practicum 1 — Application Design and Build (Domain 1)

> **Day 1 assessment · Time allowed: 45 minutes**  
> Platform: [Killercoda Kubernetes Playground](https://killercoda.com/playgrounds/scenario/kubernetes)

---

## Task 1 — Build and push a container image (10 pts)

You have been given a simple Python web server. Build it into a container image and make it available in the cluster.

**Given** — create the following `Dockerfile` in `/root/webapp/`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY server.py .
EXPOSE 8080
CMD ["python", "server.py"]
```

**Given** — create `/root/webapp/server.py`:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from CKAD practicum!\n")

HTTPServer(("", 8080), Handler).serve_forever()
```

**Steps:**

1. Build the image and tag it as `webapp:v1`.
2. Verify the image exists with `docker images`.
3. Run the image locally on port 8080 and confirm it responds with `curl localhost:8080`.

---

## Task 2 — Multi-stage build (10 pts)

Refactor the Dockerfile to use a multi-stage build:

- **Stage 1** (`builder`): use `python:3.11` to install any dependencies (add `requests` via pip).
- **Stage 2**: use `python:3.11-slim`; copy only what is needed from stage 1.

Build the final image as `webapp:v2` and verify its size is smaller than the single-stage version.

---

## Task 3 — Run a Pod from your image (10 pts)

1. Create a Pod named `webapp` in namespace `default` using image `webapp:v1`.
   - Set `imagePullPolicy: Never` (image is local).
   - Expose port `8080`.
2. Wait for the Pod to reach `Running` status.
3. Port-forward port `8080` to localhost and confirm the HTTP response.

**Expected output:** `Hello from CKAD practicum!`

---

## Task 4 — Ephemeral volume (10 pts)

Create a Pod named `logwriter` that:

- Has two containers: `writer` (image `busybox`) and `reader` (image `busybox`).
- Both containers share an `emptyDir` volume mounted at `/shared`.
- `writer` runs: `sh -c "while true; do date >> /shared/log.txt; sleep 2; done"`
- `reader` runs: `sh -c "tail -f /shared/log.txt"`

Verify that `kubectl logs logwriter -c reader` shows timestamps being written.

---

## Marking Guide

| Task | Criteria | Points |
|------|----------|--------|
| 1 | Image built, tagged, runs correctly | 10 |
| 2 | Multi-stage Dockerfile correct, image smaller | 10 |
| 3 | Pod running, port-forward returns correct body | 10 |
| 4 | Shared emptyDir, both containers running, log visible | 10 |
| **Total** | | **40** |
