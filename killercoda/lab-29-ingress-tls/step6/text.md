# Step 6: Add path-based routing

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
```bash
if see any issue then apply the patch 
kubectl patch deploy v2 --type=strategic -p='{"spec":{"template":{"spec":{"containers":[{"name":"http-echo","command":["/http-echo"],"args":["-text=hello-v2"]}]}}}}'
```
Expected: `hello-v2`.

---
