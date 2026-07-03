# Step 2: Create the application source

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
