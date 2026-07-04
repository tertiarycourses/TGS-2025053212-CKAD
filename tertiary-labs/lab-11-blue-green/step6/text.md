# Step 6: Roll back instantly (if needed)

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"blue"}}}'
```

Rollback is a single selector patch — milliseconds, no Pod churn.

---
