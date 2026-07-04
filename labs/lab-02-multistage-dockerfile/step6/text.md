# Step 6: Clean up

```bash
docker rmi demo:single demo:multi
```

---

## Free online tools

- **Distroless images** — Google's minimal runtime containers: https://github.com/GoogleContainerTools/distroless
- **Dive** — visualise image layers: https://github.com/wagoodman/dive
- **DockerHub** — browse official base images: https://hub.docker.com
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Multi-stage builds use `AS <name>` on `FROM` and `COPY --from=<name>` to transfer artifacts.
- Only the **last** `FROM` stage ends up in the final image — earlier stages are build-only.
- `CGO_ENABLED=0` produces a statically linked binary that runs in distroless/scratch.
- Smaller images = faster pulls, smaller attack surface, lower scan findings.
