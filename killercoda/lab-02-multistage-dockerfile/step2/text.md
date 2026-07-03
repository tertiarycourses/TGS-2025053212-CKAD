# Step 2: Single-stage baseline (large image)

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
