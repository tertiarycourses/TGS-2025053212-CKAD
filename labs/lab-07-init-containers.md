# Lab 7 — Init Containers

Init containers run **to completion in order** before the Pod's main containers start. They are perfect for prerequisites: waiting on a service, populating a shared volume, or doing one-time setup. In this lab you will use init containers to seed a web root and to gate on a downstream service.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Init container that seeds the web root

```bash
alias k=kubectl
cat > init.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web-init
spec:
  volumes:
  - name: html
    emptyDir: {}
  initContainers:
  - name: seed
    image: busybox
    command: ["sh","-c","echo '<h1>Seeded by init</h1>' > /work/index.html"]
    volumeMounts:
    - name: html
      mountPath: /work
  containers:
  - name: web
    image: nginx:1.25
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
EOF
k apply -f init.yaml
k get pod web-init
```

`kubectl get pod` will briefly show `Init:0/1` while the init container runs, then `Running` after it completes.

---

## Step 2 — Verify the seeded file

```bash
k exec web-init -- cat /usr/share/nginx/html/index.html
```

---

## Step 3 — Init container that waits for a Service

```bash
cat > wait.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-waiting
spec:
  initContainers:
  - name: wait-for-db
    image: busybox
    command: ["sh","-c","until nslookup db.default.svc.cluster.local; do echo waiting for db; sleep 2; done"]
  containers:
  - name: app
    image: nginx:1.25
EOF
k apply -f wait.yaml
k get pod app-waiting    # stays in Init:0/1
k logs app-waiting -c wait-for-db
```

---

## Step 4 — Create the missing Service to unblock the init container

```bash
k create service clusterip db --tcp=5432:5432
k get pod app-waiting -w     # transitions to Running, ctrl+C
```

---

## Step 5 — Clean up

```bash
k delete pod web-init app-waiting --force --grace-period 0
k delete service db
```

---

## What you learned
- Init containers run in order, to completion, before app containers start.
- They commonly seed shared volumes or wait for prerequisites.
- The Pod's status passes through `Init:N/M` until all init containers succeed.
