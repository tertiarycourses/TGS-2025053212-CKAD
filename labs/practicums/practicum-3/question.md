# Practicum 3 — Observability, Configuration & Security (Domains 3 & 4)

> **Day 3 assessment · Time allowed: 45 minutes**  
> Platform: [Killercoda Kubernetes Playground](https://killercoda.com/playgrounds/scenario/kubernetes)

---

## Task 1 — Probes (10 pts)

Create a Deployment named `probe-demo` (image `nginx:1.27`, 1 replica) with:

- **Liveness probe**: HTTP GET `/healthz` on port `80`, `initialDelaySeconds: 5`, `periodSeconds: 10`.
- **Readiness probe**: HTTP GET `/` on port `80`, `initialDelaySeconds: 3`, `periodSeconds: 5`.

Describe the Pod and confirm both probes are configured. Then deliberately break the liveness probe by exec-ing into the container and renaming `/usr/share/nginx/html/healthz` (observe the Pod restart).

---

## Task 2 — ConfigMap and Secret (15 pts)

1. Create a ConfigMap named `app-config` in namespace `default` with keys:
   - `APP_ENV=production`
   - `LOG_LEVEL=info`

2. Create a Secret named `app-secret` (type `Opaque`) with keys:
   - `DB_USER=admin`
   - `DB_PASS=s3cret`

3. Create a Pod named `config-consumer` (image `busybox`) that:
   - Loads all ConfigMap keys as environment variables.
   - Mounts the Secret as a volume at `/etc/secrets`.
   - Runs: `sh -c "env && ls /etc/secrets && sleep 3600"`

4. Exec into the Pod and verify `APP_ENV`, `LOG_LEVEL` appear in `env` output and `/etc/secrets/DB_USER` is readable.

---

## Task 3 — SecurityContext (10 pts)

Create a Pod named `secure-pod` (image `busybox`) with:

- `runAsNonRoot: true`
- `runAsUser: 1000`
- `readOnlyRootFilesystem: true`
- An `emptyDir` volume mounted at `/tmp` (so the container can still write temp files).
- Command: `sh -c "id && sleep 3600"`

Confirm the Pod starts and `kubectl exec secure-pod -- id` shows `uid=1000`.

---

## Task 4 — RBAC (5 pts)

In namespace `dev`:

1. Create a ServiceAccount named `ci-bot`.
2. Create a Role named `pod-reader` that allows `get`, `list`, `watch` on `pods`.
3. Bind `ci-bot` to `pod-reader` with a RoleBinding named `ci-bot-pod-reader`.
4. Verify with:
   ```bash
   kubectl auth can-i list pods --namespace dev --as system:serviceaccount:dev:ci-bot
   ```
   Expected: `yes`

---

## Marking Guide

| Task | Criteria | Points |
|------|----------|--------|
| 1 | Both probes configured, Pod restarts on broken liveness | 10 |
| 2 | ConfigMap env vars visible, Secret volume readable | 15 |
| 3 | Pod runs as uid 1000, read-only root FS, /tmp writable | 10 |
| 4 | RBAC chain correct, `can-i` returns yes | 5 |
| **Total** | | **40** |
