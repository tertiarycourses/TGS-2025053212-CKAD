# Step 2: Create the backend Service

```bash
kubectl create deployment web --image=hashicorp/http-echo --replicas=2 -- -text=hello-ingress
kubectl expose deployment web --port=5678 --target-port=5678
```
```bash
kubectl patch deploy web --type=json \
  -p='[{"op":"remove","path":"/spec/template/spec/containers/0/command"},
       {"op":"add","path":"/spec/template/spec/containers/0/args","value":["-text=hello-ingress"]}]'
```
---
