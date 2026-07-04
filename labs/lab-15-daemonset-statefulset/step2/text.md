# Step 2: DaemonSet on every node

```bash
cat > ds.yaml <<'EOF'
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-agent
spec:
  selector:
    matchLabels:
      app: node-agent
  template:
    metadata:
      labels:
        app: node-agent
    spec:
      tolerations:
      - operator: Exists
      containers:
      - name: agent
        image: busybox
        command: ["sh", "-c", "while true; do echo agent on $(hostname); sleep 30; done"]
EOF
k apply -f ds.yaml
k get ds,pods -l app=node-agent -o wide
```

`tolerations: - operator: Exists` schedules the DaemonSet Pod on control-plane nodes too — required in Killercoda's single-node setup. The `DESIRED` count matches the node count.

---
