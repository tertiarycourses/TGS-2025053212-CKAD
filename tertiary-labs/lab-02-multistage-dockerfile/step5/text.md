# Step 5: Run the small image and test

```bash
docker run -d --name multi -p 8080:8080 demo:multi
curl http://localhost:8080
docker rm -f multi
```

Expected response: `hello from multi-stage build`

---
