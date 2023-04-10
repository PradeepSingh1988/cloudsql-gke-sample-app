resource "kubernetes_namespace" "sample_app" {
  metadata {
    name = var.gke_namespace
  }
}

module "my-app-workload-identity" {
  source     = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  name       = var.gcp_sa
  namespace  = kubernetes_namespace.sample_app.metadata[0].name
  project_id = var.project_id

  # roles/cloudsql.instanceUser is required when you login using IAM
  roles = ["roles/cloudsql.client", "roles/cloudsql.instanceUser"]
}

# This is just to configure the grants to databases

resource "kubernetes_namespace" "sql_admin_namespace" {
  metadata {
    name = "sql-admin-ns"
  }
}
module "sql-admin-workload-identity" {
  source     = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  name       = "sql-admin"
  namespace  = kubernetes_namespace.sql_admin_namespace.metadata[0].name
  project_id = var.project_id
  roles      = ["roles/cloudsql.admin"]
}
