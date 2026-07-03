# Step 5: Test HTTPS routing

```bash
curl -k --resolve demo.local:$HTTPS_PORT:127.0.0.1 \
  https://demo.local:$HTTPS_PORT/
```

Expected: `hello-ingress`. `--resolve` overrides DNS so the Host header matches the Ingress rule. `-k` skips self-signed cert verification.

---
