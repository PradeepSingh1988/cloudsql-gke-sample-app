resource "kubernetes_namespace" "sample_app" {
  metadata {
    name = "sample-app"
  }
}


module "my-app-workload-identity" {
  source     = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  name       = "sample-app"
  namespace  = kubernetes_namespace.sample_app.metadata[0].name
  project_id = var.project_id
  roles      = ["roles/cloudsql.client"]
}
