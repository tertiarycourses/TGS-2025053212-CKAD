# Step 6: Disable token auto-mount (least privilege)

```bash
k patch sa app-sa -p '{"automountServiceAccountToken": false}'
```

Set this on Pods or ServiceAccounts that do not need API access. It removes the projected volume from the Pod.

---
