# Step 3: Trigger a liveness failure

```bash
k exec web-probes -- rm /usr/share/nginx/html/index.html
sleep 35
k get pod web-probes
```

After `failureThreshold: 3` failed probes the container is restarted. Watch the `RESTARTS` counter increment.

---
