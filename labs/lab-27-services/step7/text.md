# Step 7: Debug a selector mismatch

```bash
k patch svc web-cip -p '{"spec":{"selector":{"app":"does-not-exist"}}}'
k get endpoints web-cip
k patch svc web-cip -p '{"spec":{"selector":{"app":"web"}}}'
```

Empty Endpoints = selector does not match any Pod labels. This is the most common Service bug on the exam.

---
