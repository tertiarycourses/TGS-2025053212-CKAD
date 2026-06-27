# Lab 25 — RBAC (Role and RoleBinding)

RBAC controls who can do what on which resources. CKAD 2026 tests creating Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings imperatively, and validating with `kubectl auth can-i --as`. You must know the difference between namespace-scoped and cluster-scoped permissions.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create a namespace and ServiceAccount

```bash
k create namespace dev
k create serviceaccount viewer -n dev
```

---

## Step 3 — Role: namespace-scoped permissions

```bash
k create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n dev
k describe role pod-reader -n dev
```

A `Role` is always scoped to one namespace. Verbs: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, `deletecollection`.

---

## Step 4 — RoleBinding: link Role to ServiceAccount

```bash
k create rolebinding viewer-binding \
  --role=pod-reader \
  --serviceaccount=dev:viewer \
  -n dev
k describe rolebinding viewer-binding -n dev
```

---

## Step 5 — Validate with kubectl auth can-i

```bash
k auth can-i list pods   -n dev     --as=system:serviceaccount:dev:viewer
k auth can-i delete pods -n dev     --as=system:serviceaccount:dev:viewer
k auth can-i list pods   -n default --as=system:serviceaccount:dev:viewer
```

Expected: `yes`, `no`, `no`. The Role only covers the `dev` namespace.

---

## Step 6 — ClusterRole + ClusterRoleBinding (cluster-wide)

```bash
k create clusterrole node-reader --verb=get,list --resource=nodes
k create serviceaccount nodes-sa -n dev
k create clusterrolebinding nodes-binding \
  --clusterrole=node-reader \
  --serviceaccount=dev:nodes-sa
k auth can-i list nodes --as=system:serviceaccount:dev:nodes-sa
```

Expected: `yes`. A ClusterRole bound via ClusterRoleBinding grants permission in all namespaces.

---

## Step 7 — ClusterRole + RoleBinding (one namespace only)

```bash
k create rolebinding dev-node-reader \
  --clusterrole=node-reader \
  --serviceaccount=dev:viewer \
  -n dev
k auth can-i list nodes -n dev --as=system:serviceaccount:dev:viewer
```

A ClusterRole used with a RoleBinding limits permissions to the binding's namespace — a common exam pattern.

---

## Step 8 — RBAC verb reference

| Verb | HTTP Method | Use Case |
|------|-------------|----------|
| `get` | GET (single) | Read one object |
| `list` | GET (collection) | List all objects |
| `watch` | GET (watch) | Stream change events |
| `create` | POST | Create a new object |
| `update` | PUT | Full replace |
| `patch` | PATCH | Partial update |
| `delete` | DELETE | Delete one object |
| `deletecollection` | DELETE | Delete many |

---

## Step 9 — Clean up

```bash
k delete clusterrolebinding nodes-binding
k delete clusterrole node-reader
k delete namespace dev
```

---

## Free online tools

- **RBAC docs**: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- **kubectl auth can-i reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth_can-i/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `Role` + `RoleBinding` = namespace-scoped permissions.
- `ClusterRole` + `ClusterRoleBinding` = cluster-wide permissions.
- `ClusterRole` + `RoleBinding` = cluster role's verbs limited to one namespace.
- `kubectl auth can-i <verb> <resource> --as=<identity>` validates without authenticating.
