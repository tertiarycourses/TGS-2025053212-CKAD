# Lab 1 — Build a Container Image with Docker

In this lab you will write a small Dockerfile, build a container image, and run it locally. The CKAD exam expects you to understand image construction even though you usually consume pre-built images. By the end you will be able to point at any layer in a Dockerfile and explain what it produces.

Run all commands on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Verify Docker is available

Killercoda's Kubernetes VM ships with the `docker` CLI alongside `containerd`.

```bash
docker version
docker info | head -20
```

If `docker version` prints a Client and Server section, the daemon is running.

---

## Step 2 — Create a tiny web app

```bash
mkdir -p ~/lab01 && cd ~/lab01

cat > app.py <<'EOF'
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"hello from CKAD lab 1\n")
HTTPServer(("0.0.0.0", 8080), H).serve_forever()
EOF
```

---

## Step 3 — Write the Dockerfile

```bash
cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF
```

Flag breakdown:
- `FROM` — base image layer
- `WORKDIR` — sets and creates the working directory
- `COPY` — copy build context into the image
- `EXPOSE` — documentation only, does not publish ports
- `CMD` — default process when the container starts

---

## Step 4 — Build the image

```bash
docker build -t ckad/hello:1.0 .
```

The `-t` flag tags the image. The trailing `.` is the build context (current directory).

---

## Step 5 — Run the container

```bash
docker run -d --name hello -p 8080:8080 ckad/hello:1.0
curl http://localhost:8080
```

Expected output:

```
hello from CKAD lab 1
```

---

## Step 6 — Inspect the image

```bash
docker images ckad/hello
docker history ckad/hello:1.0
```

`docker history` shows one row per Dockerfile instruction — proof that each line becomes a layer.

---

## Step 7 — Clean up

```bash
docker rm -f hello
docker rmi ckad/hello:1.0
```

---

## What you learned
- The four most-tested Dockerfile instructions: `FROM`, `WORKDIR`, `COPY`, `CMD`.
- How `docker build`, `docker run`, and `docker history` map to image layers.
- Why `EXPOSE` is documentation and `-p` is what actually publishes a port.
