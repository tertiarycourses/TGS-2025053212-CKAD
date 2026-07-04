# Step 3: Generate a self-signed TLS certificate

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
k create secret tls demo-tls --cert=tls.crt --key=tls.key
k get secret demo-tls -o jsonpath='{.type}'; echo
```

---
