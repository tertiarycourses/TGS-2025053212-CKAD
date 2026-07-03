# Step 4: Inspect the auto-mounted token inside the Pod

```bash
k exec app -- ls /var/run/secrets/kubernetes.io/serviceaccount/
k exec app -- sh -c 'cat /var/run/secrets/kubernetes.io/serviceaccount/namespace; echo'
```

Three files are projected: `token`, `ca.crt`, and `namespace`. The token is a short-lived JWT rotated automatically by the kubelet.

---
