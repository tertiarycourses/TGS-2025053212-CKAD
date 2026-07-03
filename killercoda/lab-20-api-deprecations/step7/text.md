# Step 7: Stable API version reference (Kubernetes v1.35)

| Resource | apiVersion |
|----------|------------|
| Pod, Service, ConfigMap, Secret, Namespace, ServiceAccount | `v1` |
| Deployment, StatefulSet, DaemonSet, ReplicaSet | `apps/v1` |
| Job, CronJob | `batch/v1` |
| Ingress, NetworkPolicy | `networking.k8s.io/v1` |
| Role, RoleBinding, ClusterRole, ClusterRoleBinding | `rbac.authorization.k8s.io/v1` |
| HorizontalPodAutoscaler | `autoscaling/v2` |
| PodDisruptionBudget | `policy/v1` |
| ResourceQuota, LimitRange | `v1` |

---
