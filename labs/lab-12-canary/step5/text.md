# Step 5: Promote: scale up canary, retire stable

```bash
k scale deployment web-canary --replicas=9
k scale deployment web-stable --replicas=0
```

Once the canary is fully promoted, delete the stable Deployment.

---
