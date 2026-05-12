# Lab 29 — Ingress with TLS

An Ingress is L7 routing: hostnames and paths to Services, optionally terminating TLS. In this lab you will install ingress-nginx, create a self-signed cert, and route HTTPS traffic to a backend.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Install ingress-nginx

```bash
alias k=kubectl
k apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml
k -n ingress-nginx rollout status deployment/ingress-nginx-controller
HTTP_PORT=$(k -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.spec.ports[?(@.name=="http")].nodePort}')
HTTPS_PORT=$(k -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
echo "HTTP=$HTTP_PORT  HTTPS=$HTTPS_PORT"
```

---

## Step 2 — Backend service

```bash
k create deployment web --image=hashicorp/http-echo --replicas=2 -- -text=hello-ingress
k expose deployment web --port=5678 --target-port=5678
```

---

## Step 3 — Self-signed TLS Secret

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 1 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
k create secret tls demo-tls --cert=tls.crt --key=tls.key
```

---

## Step 4 — Ingress with TLS and host routing

```bash
cat > ing.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo
spec:
  ingressClassName: nginx
  tls:
  - hosts: [ "demo.local" ]
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

---

## Step 5 — Hit the Ingress

```bash
curl -k --resolve demo.local:$HTTPS_PORT:127.0.0.1 https://demo.local:$HTTPS_PORT/
```

`--resolve` overrides DNS so the Host header matches what the Ingress expects.

---

## Step 6 — Path-based routing

```bash
k create deployment v2 --image=hashicorp/http-echo -- -text=hello-v2
k expose deployment v2 --port=5678 --target-port=5678

k patch ing demo --type=json -p='[
{"op":"add","path":"/spec/rules/0/http/paths/-","value":{"path":"/v2","pathType":"Prefix","backend":{"service":{"name":"v2","port":{"number":5678}}}}}]'

curl -k --resolve demo.local:$HTTPS_PORT:127.0.0.1 https://demo.local:$HTTPS_PORT/v2
```

---

## Step 7 — Clean up

```bash
k delete ing demo
k delete svc web v2
k delete deployment web v2
k delete secret demo-tls
k delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/baremetal/deploy.yaml
rm tls.crt tls.key
```

---

## What you learned
- Install ingress-nginx in one command.
- Ingress `tls:` block + `kubernetes.io/tls` Secret = HTTPS termination.
- Host- and path-based routing with `pathType: Prefix`.
