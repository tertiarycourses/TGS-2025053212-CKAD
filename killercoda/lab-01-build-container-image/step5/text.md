# Step 5: Run and test the container

```bash
docker run -d --name hello -p 8080:5000 ckad/hello:1.0
curl http://localhost:8080
docker rm -f hello
docker run --name hello -p 8080:8080 ckad/hello:1.0
hello


```

Expected response:
```

The server is running — the terminal is now blocked (that's normal for foreground mode). Open a second terminal on Killercoda and run:

curl http://localhost:8080

You should get hello from CKAD 2026 lab 1. Once confirmed, press Ctrl+C in the first terminal to stop it, then restart with -d to run it in the background.

hello from CKAD 2026 lab 1
```

`-p 8080:8080` maps `host:container` — this is what actually publishes the port, not `EXPOSE`.

---
