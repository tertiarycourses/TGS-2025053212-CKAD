# Lab 2 — Multi-Stage Dockerfile

Separate the build stage from the runtime stage to produce images that are 10× smaller and contain no compiler toolchain. Multi-stage builds are a CKAD 2026 exam staple — you must be able to write one from scratch and explain why it shrinks the image.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `docker` (pre-installed on Killercoda)
- `golang:1.22` builder image (pulled automatically)
- `gcr.io/distroless/static-debian12` runtime image (pulled automatically)

---

## Step 1 — Create the Go source file

```bash
mkdir -p ~/lab02 && cd ~/lab02

cat > main.go <<'EOF'
package main
import ("fmt"; "net/http")
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "hello from multi-stage build")
    })
    http.ListenAndServe(":8080", nil)
}
EOF
```

---

## Step 2 — Single-stage baseline (large image)

```bash
cat > Dockerfile.single <<'EOF'
FROM golang:1.22
WORKDIR /src
COPY main.go .
RUN go mod init demo && go build -o app main.go
CMD ["./app"]
EOF
docker build -f Dockerfile.single -t demo:single .
```

This image ships the entire Go toolchain (~800 MB) just to run a 6 MB binary.

---

## Step 3 — Multi-stage Dockerfile (small image)

```bash
cat > Dockerfile.multi <<'EOF'
# Stage 1: compile
FROM golang:1.22 AS builder
WORKDIR /src
COPY main.go .
RUN go mod init demo && CGO_ENABLED=0 go build -o /out/app main.go

# Stage 2: runtime only
FROM gcr.io/distroless/static-debian12
COPY --from=builder /out/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
EOF
docker build -f Dockerfile.multi -t demo:multi .
```

`COPY --from=builder` pulls only the compiled binary into the final image. The entire Go toolchain stays in the builder stage and is discarded.

---

## Step 4 — Compare image sizes

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

## Step 5 — Run the small image and test

```bash
docker run -d --name multi -p 8080:8080 demo:multi
curl http://localhost:8080
docker rm -f multi
```

Expected response: `hello from multi-stage build`

---

## Step 6 — Clean up

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
