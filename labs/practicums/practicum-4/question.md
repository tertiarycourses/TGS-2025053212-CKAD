# Practicum 4 — Services, Networking & Final Mock Assessment (Domain 5)

> **Day 4 assessment · Time allowed: 2 hours**  
> Platform: [Killercoda Kubernetes Playground](https://killercoda.com/playgrounds/scenario/kubernetes)  
> This is the final summative assessment covering all 5 CKAD domains.

---

## Part A — Services and Networking (Domain 5) — 40 pts

### Task A1 — ClusterIP and NodePort (15 pts)

1. Create a Deployment `web` (image `nginx:1.27`, 2 replicas) with label `app=web`.
2. Expose it as a **ClusterIP** Service named `web-internal` on port `80`.
3. Expose it as a **NodePort** Service named `web-external` on port `80`, nodePort `30080`.
4. Verify ClusterIP access from another Pod via DNS: `curl web-internal.default.svc.cluster.local`.
5. Verify NodePort access: `curl <NodeIP>:30080`.

### Task A2 — Ingress with TLS (15 pts)

1. Install the ingress-nginx controller (use the quick manifest):
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml
   ```
2. Create a self-signed TLS certificate for `demo.local`:
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout tls.key -out tls.crt -subj "/CN=demo.local"
   kubectl create secret tls demo-tls --cert=tls.crt --key=tls.key
   ```
3. Create an Ingress resource that routes `demo.local/` → `web-internal:80` using TLS.
4. Test with: `curl -k --resolve demo.local:443:<IngressIP> https://demo.local`.

### Task A3 — NetworkPolicy (10 pts)

Create a NetworkPolicy named `deny-all` in namespace `default` that:
- Denies all ingress to Pods with label `app=web`.
- Then create a second policy `allow-from-frontend` that permits ingress on port `80` only from Pods with label `role=frontend`.

Verify by running a curl from a `role=frontend` Pod (should succeed) and from a Pod without that label (should fail/timeout).

---

## Part B — Integrated Scenario (all domains) — 60 pts

Deploy a minimal two-tier application: a **backend API** and a **frontend** that calls it, with proper RBAC, resource limits, and health probes.

### Task B1 — Backend Deployment (20 pts)

Create namespace `app`.

Deploy `backend`:
- Image: `kennethreitz/httpbin` (echo server)
- 2 replicas, label `tier=backend`
- Liveness probe: HTTP GET `/get` port `80`, delay `10s`, period `15s`
- Readiness probe: HTTP GET `/get` port `80`, delay `5s`, period `10s`
- Resource requests: `cpu: 100m`, `memory: 64Mi`
- Resource limits: `cpu: 250m`, `memory: 128Mi`
- ConfigMap `backend-config` with `LOG_LEVEL=debug` injected as env var

Expose as ClusterIP Service `backend-svc` on port `80`.

### Task B2 — Frontend Deployment (15 pts)

Deploy `frontend`:
- Image: `nginx:1.27`, 1 replica, label `tier=frontend, role=frontend`
- ConfigMap `frontend-config` with `BACKEND_URL=http://backend-svc.app.svc.cluster.local`
  mounted as file `/etc/nginx/conf.d/upstream.conf`
- Resource requests: `cpu: 50m`, `memory: 32Mi`

Expose as NodePort Service `frontend-svc` on port `80`, nodePort `30090`.

### Task B3 — RBAC and ServiceAccount (10 pts)

In namespace `app`:
1. Create ServiceAccount `app-monitor`.
2. Create ClusterRole `pod-log-reader` allowing `get`, `list` on `pods` and `pods/log`.
3. Bind `app-monitor` to `pod-log-reader` in namespace `app`.
4. Run a Pod `monitor` using ServiceAccount `app-monitor` and verify it can list pods:
   ```bash
   kubectl exec monitor -- kubectl get pods -n app
   ```

### Task B4 — PersistentVolume and PVC (15 pts)

1. Create a PersistentVolume `app-pv` with `hostPath /data/app`, capacity `1Gi`, accessMode `ReadWriteOnce`.
2. Create a PersistentVolumeClaim `app-pvc` requesting `500Mi`.
3. Mount `app-pvc` into the `backend` Deployment at `/data`.
4. Exec into a backend Pod and write a test file: `echo "ckad" > /data/test.txt`.
5. Delete the Pod and verify the file persists in the new replacement Pod.

---

## Marking Guide

| Section | Task | Points |
|---------|------|--------|
| Part A | A1 — ClusterIP + NodePort | 15 |
| Part A | A2 — Ingress + TLS | 15 |
| Part A | A3 — NetworkPolicy | 10 |
| Part B | B1 — Backend Deployment | 20 |
| Part B | B2 — Frontend Deployment | 15 |
| Part B | B3 — RBAC | 10 |
| Part B | B4 — PV/PVC | 15 |
| **Total** | | **100** |

**Pass mark: 70/100**
