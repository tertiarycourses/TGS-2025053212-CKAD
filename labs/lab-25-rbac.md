# Lab 25 — RBAC (Role and RoleBinding)

RBAC controls **who** can do **what** on **which** resources. In this lab you will create a Role, bind it to a ServiceAccount with a RoleBinding, and verify with `kubectl auth can-i`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create a ServiceAccount in a fresh namespace

```bash
alias k=kubectl
k create namespace dev
k create serviceaccount viewer -n dev
```

---

## Step 2 — Role that allows reading Pods

```bash
k create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n dev
k describe role pod-reader -n dev
```

---

## Step 3 — RoleBinding linking the Role to the SA

```bash
k create rolebinding viewer-binding \
  --role=pod-reader \
  --serviceaccount=dev:viewer \
  -n dev
```

---

## Step 4 — Test with `kubectl auth can-i`

```bash
k auth can-i list pods   -n dev --as=system:serviceaccount:dev:viewer
k auth can-i delete pods -n dev --as=system:serviceaccount:dev:viewer
k auth can-i list pods   -n default --as=system:serviceaccount:dev:viewer
```

Expected: `yes`, `no`, `no`.

---

## Step 5 — Cluster-scoped: ClusterRole + ClusterRoleBinding

```bash
k create clusterrole node-reader --verb=get,list --resource=nodes
k create serviceaccount nodes-sa -n dev
k create clusterrolebinding nodes-binding \
  --clusterrole=node-reader \
  --serviceaccount=dev:nodes-sa
k auth can-i list nodes --as=system:serviceaccount:dev:nodes-sa
```

ClusterRole + ClusterRoleBinding = cluster-wide permission. ClusterRole + RoleBinding = the cluster role's verbs limited to one namespace.

---

## Step 6 — Verbs cheat-sheet

| Verb | What it allows |
|------|---------------|
| get | Read a single object |
| list | List objects (also includes get on collection) |
| watch | Stream changes |
| create | POST a new object |
| update | PUT an existing object |
| patch | PATCH (partial update) |
| delete | DELETE a single object |
| deletecollection | DELETE many |

---

## Step 7 — Clean up

```bash
k delete clusterrolebinding nodes-binding
k delete clusterrole node-reader
k delete namespace dev
```

---

## What you learned
- Role + RoleBinding (namespaced) vs ClusterRole + ClusterRoleBinding (cluster-wide).
- `kubectl create role|rolebinding|clusterrole|clusterrolebinding` imperative shortcuts.
- `kubectl auth can-i ... --as=` to verify RBAC without logging in.
