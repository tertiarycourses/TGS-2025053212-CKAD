# Step 7: Clean up

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
