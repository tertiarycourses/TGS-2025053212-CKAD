# Step 3: Write the Dockerfile

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
