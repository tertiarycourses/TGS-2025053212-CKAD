# Lab 1 — Build a Container Image with Docker

Write a Dockerfile from scratch, build a tagged image, run it locally, and inspect its layers. The CKAD 2026 exam expects you to read and write Dockerfiles confidently — you may be asked to fix a broken one or produce one under time pressure.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `docker` (pre-installed on Killercoda)
- `python:3.12-slim` base image (pulled automatically on first build)

---

## Step 1 — Verify the environment

```bash
docker version
kubectl get nodes
```

Confirm Docker Client + Server are both shown and at least one node is `Ready` before continuing.

---

## Step 2 — Create the application source

```bash
mkdir -p ~/lab01 && cd ~/lab01

cat > app.py <<'EOF'
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"hello from CKAD 2026 lab 1\n")
    def log_message(self, *a): pass
HTTPServer(("0.0.0.0", 8080), H).serve_forever()
EOF
```

Verify: `ls ~/lab01` should show `app.py`.

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

Key instructions tested in CKAD 2026:
- `FROM` — selects the base layer; always pin a version tag
- `WORKDIR` — creates and cd's into the directory in one line
- `COPY` — copies from build context into the image filesystem
- `EXPOSE` — documentation only; does **not** publish the port
- `CMD` — default command; overridden by anything after `docker run <image> ...`

---

## Step 4 — Build and tag the image

```bash
docker build -t ckad/hello:1.0 .
```

The `-t` flag sets the tag (`name:version`). The trailing `.` is the build context — the directory whose files `COPY` can access. Expect 30–60 seconds on first run while the base image downloads.

---

## Step 5 — Run and test the container

```bash
docker run -d --name hello -p 8080:5000 ckad/hello:1.0
curl http://localhost:8080
docker rm -f hello
docker run --name hello -p 8080:8080 ckad/hello:1.0
hello


```

Expected response:
```

The server is running — the terminal is now blocked (that's normal for foreground mode). Open a second terminal on Killercoda and run:

curl http://localhost:8080

You should get hello from CKAD 2026 lab 1. Once confirmed, press Ctrl+C in the first terminal to stop it, then restart with -d to run it in the background.

hello from CKAD 2026 lab 1
```

`-p 8080:8080` maps `host:container` — this is what actually publishes the port, not `EXPOSE`.

---

## Step 6 — Inspect the image layers

```bash
docker images ckad/hello
docker history ckad/hello:1.0
```

`docker history` prints one row per instruction. Use it to prove each Dockerfile line becomes a distinct layer.

---

## Step 7 — Clean up

```bash
docker rm -f hello
docker rmi ckad/hello:1.0
```

Verify: `docker ps -a | grep hello` and `docker images | grep hello` should both return no output.

---

## Free online tools

- **Dockerfile reference** — official instruction docs: https://docs.docker.com/reference/dockerfile/
- **DockerHub** — search for base images: https://hub.docker.com
- **Play with Docker** — alternative browser Docker environment: https://labs.play-with-docker.com
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- The five most-tested Dockerfile instructions: `FROM`, `WORKDIR`, `COPY`, `EXPOSE`, `CMD`.
- `EXPOSE` is metadata only — `-p host:container` is what opens the port.
- `docker history` maps directly to Dockerfile lines — one instruction, one layer.
- Always pin base image tags (`python:3.12-slim` not `python:latest`) for reproducible builds.
