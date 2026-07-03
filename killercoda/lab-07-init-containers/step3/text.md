# Step 3: Verify the seeded content

```bash
k exec web-init -- cat /usr/share/nginx/html/index.html
```

Expected: `<h1>Seeded by init container</h1>`

---
