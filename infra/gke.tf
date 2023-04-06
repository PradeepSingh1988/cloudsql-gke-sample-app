data "google_project" "project" {
  project_id = var.project_id
}


module "gke" {
  source                   = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  project_id               = var.project_id
  name                     = "asm-cluster"
  regional                 = true
  region                   = var.region
  release_channel          = "REGULAR"
  network_project_id       = var.network_project_id
  network                  = var.shared_vpc_name
  subnetwork               = var.subnet_name
  ip_range_pods            = var.pods_range
  ip_range_services        = var.services_range
  create_service_account   = false
  service_account          = var.gke_node_service_account
  network_policy           = false
  cluster_resource_labels  = { "mesh_id" : "proj-${data.google_project.project.number}" }
  identity_namespace       = "${var.project_id}.svc.id.goog"
  remove_default_node_pool = true
  enable_private_nodes     = true
  enable_private_endpoint  = false
  node_pools = [
    {
      name            = "asm-node-pool"
      autoscaling     = false
      auto_upgrade    = true
      node_count      = 1
      machine_type    = "e2-standard-4"
      service_account = var.gke_node_service_account
    },
  ]
}

module "asm" {
  source                    = "terraform-google-modules/kubernetes-engine/google//modules/asm"
  project_id                = var.project_id
  cluster_name              = module.gke.name
  cluster_location          = module.gke.location
  multicluster_mode         = "connected"
  enable_cni                = true
  enable_fleet_registration = true
  enable_mesh_feature       = true
}
