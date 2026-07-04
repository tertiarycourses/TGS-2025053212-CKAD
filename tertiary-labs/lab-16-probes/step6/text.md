# Step 6: Clean up

```bash
k delete pod web-probes db-probe slow --force --grace-period=0
```

---

## Free online tools

- **Probes docs**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- **Probe field reference**: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#ProbeHandler
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Three probe types: `httpGet`, `tcpSocket`, `exec` — pick by what the container exposes.
- `initialDelaySeconds` + `periodSeconds` + `failureThreshold` control probe timing.
- `startupProbe` blocks liveness and readiness until the app is fully initialised.
- `readinessProbe` failure removes the Pod from Service endpoints without restarting it.
