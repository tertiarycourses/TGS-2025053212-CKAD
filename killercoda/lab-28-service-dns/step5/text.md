# Step 5: Pod DNS record

```bash
POD_IP=$(k -n app get pod -l app=web -o jsonpath='{.items[0].status.podIP}')
DASHED=$(echo $POD_IP | tr . -)
k -n probe run client --image=busybox --restart=Never -it --rm -- \
  nslookup $DASHED.app.pod.cluster.local
```

Every Pod gets a DNS A record: `<dashed-ip>.<namespace>.pod.cluster.local`.

---
