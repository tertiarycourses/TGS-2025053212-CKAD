# Step 6: Aggregate logs across a Deployment

```bash
k create deployment fleet --image=busybox --replicas=3 \
  -- sh -c 'while true; do echo $(hostname); sleep 1; done'
sleep 5
k logs deployment/fleet --tail=3
k logs -l app=fleet --prefix=true --tail=2
```

`-l <selector>` targets all Pods matching the label — no need to know individual Pod names.

---
