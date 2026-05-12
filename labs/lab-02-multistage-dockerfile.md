# Lab 2 — Multi-Stage Dockerfile

In this lab you will shrink an image by separating the **build** stage from the **runtime** stage. Multi-stage builds are the standard CKAD pattern for producing small, secure images. You will see a roughly 10× reduction in size by discarding compilers and source code.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Source code

```bash
mkdir -p ~/lab02 && cd ~/lab02

cat > main.go <<'EOF'
package main
import ("fmt"; "net/http")
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request){
        fmt.Fprintln(w, "hello from multi-stage build")
    })
    http.ListenAndServe(":8080", nil)
}
EOF
```

---

## Step 2 — Single-stage Dockerfile (baseline)

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

---

## Step 3 — Multi-stage Dockerfile

```bash
cat > Dockerfile.multi <<'EOF'
# --- build stage ---
FROM golang:1.22 AS builder
WORKDIR /src
COPY main.go .
RUN go mod init demo && CGO_ENABLED=0 go build -o /out/app main.go

# --- runtime stage ---
FROM gcr.io/distroless/static-debian12
COPY --from=builder /out/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
EOF
docker build -f Dockerfile.multi -t demo:multi .
```

Key idea: `COPY --from=builder` pulls only the compiled binary into a tiny final image. The Go toolchain stays behind.

---

## Step 4 — Compare sizes

```bash
docker images | grep demo
```

You should see `demo:single` around **800 MB** and `demo:multi` around **8–10 MB**.

---

## Step 5 — Run the small image

```bash
docker run -d --name multi -p 8080:8080 demo:multi
curl http://localhost:8080
docker rm -f multi
```

---

## What you learned
- Why multi-stage builds shrink images dramatically.
- How `COPY --from=<stage>` selects a previous stage.
- Why distroless / scratch images are preferred for runtime stages.
