# Step 3: Multi-stage Dockerfile (small image)

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
