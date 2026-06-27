# Lab 29 — Ingress with TLS

An Ingress provides Layer 7 (HTTP/HTTPS) routing: hostname and path rules that forward traffic to backend Services. CKAD 2026 tests installing an Ingress controller, creating TLS Secrets, host routing, and path-based routing with `pathType`.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `openssl` (pre-installed on Killercoda)
- ingress-nginx controller (installed in Step 1)
- `hashicorp/http-echo` image (pulled automatically)

---

## Step 1 — Install ingress-nginx controller

```bash
alias k=kubectl
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml
kubectl -n ingress-nginx rollout status deployment/ingress-nginx-controller
HTTP_PORT=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
  -o jsonpath='{.spec.ports[?(@.name=="http")].nodePort}')
HTTPS_PORT=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
  -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
echo "HTTP=$HTTP_PORT  HTTPS=$HTTPS_PORT"
```

---

## Step 2 — Create the backend Service

```bash
k create deployment web --image=hashicorp/http-echo --replicas=2 \
  -- -text=hello-ingress
k expose deployment web --port=5678 --target-port=5678
```

---

## Step 3 — Generate a self-signed TLS certificate

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
k create secret tls demo-tls --cert=tls.crt --key=tls.key
k get secret demo-tls -o jsonpath='{.type}'; echo
```

---

## Step 4 — Create the Ingress with TLS and host routing

```bash
cat > ing.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - demo.local
    secretName: demo-tls
  rules:
  - host: demo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 5678
EOF
k apply -f ing.yaml
k get ing demo
```

Key fields: `ingressClassName: nginx` (selects the controller), `tls.secretName` (points at your TLS Secret), `pathType: Prefix` (matches `/` and anything below).

---

## Step 5 — Test HTTPS routing

```bash
curl -k --resolve demo.local:$HTTPS_PORT:127.0.0.1 \
  https://demo.local:$HTTPS_PORT/
```

Expected: `hello-ingress`. `--resolve` overrides DNS so the Host header matches the Ingress rule. `-k` skips self-signed cert verification.

---

## Step 6 — Add path-based routing

```bash
k create deployment v2 --image=hashicorp/http-echo -- -text=hello-v2
k expose deployment v2 --port=5678 --target-port=5678

kubectl patch ing demo --type=json -p='[
  {"op":"add","path":"/spec/rules/0/http/paths/-",
   "value":{"path":"/v2","pathType":"Prefix",
   "backend":{"service":{"name":"v2","port":{"number":5678}}}}}]'

curl -k --resolve demo.local:$HTTPS_PORT:127.0.0.1 \
  https://demo.local:$HTTPS_PORT/v2
```

Expected: `hello-v2`.

---

## Step 7 — Clean up

```bash
k delete ing demo
k delete svc web v2
k delete deployment web v2
k delete secret demo-tls
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml
rm -f tls.crt tls.key
```

---

## Free online tools

- **Ingress docs**: https://kubernetes.io/docs/concepts/services-networking/ingress/
- **ingress-nginx docs**: https://kubernetes.github.io/ingress-nginx/
- **Ingress controllers list**: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Ingress `apiVersion` is `networking.k8s.io/v1` (not `extensions/v1beta1` — removed in 1.22).
- `ingressClassName` selects which controller handles the Ingress.
- `tls.secretName` must point to a `kubernetes.io/tls` type Secret.
- `pathType: Prefix` matches the path and all sub-paths; `Exact` requires an exact match.
- `--resolve` and `-k` in curl allow testing Ingress without real DNS or a valid certificate.
