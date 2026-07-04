# Step 6: Exceed the ResourceQuota

```bash
for i in 1 2 3 4; do k run quota-$i --image=nginx:1.25 -n team-a; done
k run quota-5 --image=nginx:1.25 -n team-a 2>&1 | head -3
```

The 6th Pod (pods quota is `5`) is rejected: `exceeded quota: team-a-quota`.

---
