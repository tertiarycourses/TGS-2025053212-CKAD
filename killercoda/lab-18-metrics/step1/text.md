# Step 1: Install metrics-server

```bash
alias k=kubectl
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Killercoda uses self-signed kubelet certificates, so patch the Deployment to skip TLS verification:

```bash
kubectl patch -n kube-system deployment metrics-server --type=json -p='
[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deployment/metrics-server
```

Wait for the API to become available:

```bash
until kubectl top node 2>/dev/null; do echo "waiting for metrics..."; sleep 5; done
```

---
