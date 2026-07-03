# Step 7: Headless Service returns all Pod IPs

```bash
k -n app create service clusterip headless --clusterip="None" --tcp=80:80
k -n app patch service headless -p '{"spec":{"selector":{"app":"web"}}}'
k -n probe run h --image=busybox --restart=Never -it --rm -- nslookup headless.app
```

A headless Service (`clusterIP: None`) returns all Pod IPs in DNS instead of a single virtual IP.

---
