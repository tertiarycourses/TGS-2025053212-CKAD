# Step 4: NodePort Service (exposes a port on every node)

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=NodePort --name=web-np
PORT=$(k get svc web-np -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort=$PORT"
curl -s http://localhost:$PORT | head -3
```

NodePort opens the same TCP port (30000–32767 range) on every node in the cluster.

---
