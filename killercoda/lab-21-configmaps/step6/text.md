# Step 6: Live update (file mount vs env var)

```bash
k create configmap app-conf \
  --from-file=app.conf=<(echo "debug=false") \
  --dry-run=client -o yaml | k apply -f -
sleep 60
k exec vol -- cat /etc/app/app.conf
```

The file mount updates automatically within ~60 seconds. Environment variable injections are **fixed at Pod startup** — to refresh them you must delete and recreate the Pod.

---
