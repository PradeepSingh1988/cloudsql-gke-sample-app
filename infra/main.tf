locals {
  cluster_output_master_auth      = concat(data.google_container_cluster.primary.*.master_auth, [])
  cluster_master_auth_list_layer1 = local.cluster_output_master_auth
  cluster_master_auth_list_layer2 = local.cluster_master_auth_list_layer1[0]
  cluster_master_auth_map         = local.cluster_master_auth_list_layer2[0]
  cluster_ca_certificate          = local.cluster_master_auth_map["cluster_ca_certificate"]
  cluster_endpoint                = data.google_container_cluster.primary.private_cluster_config[0].public_endpoint
}

provider "kubernetes" {
  host                   = "https://${local.cluster_endpoint}"
  token                  = data.google_client_config.default_config.access_token
  cluster_ca_certificate = base64decode(local.cluster_ca_certificate)
}

data "google_client_config" "default_config" {}

data "google_compute_network" "shared-vpc" {
  name    = var.shared_vpc_name
  project = var.network_project_id
}

data "google_container_cluster" "primary" {
  name     = var.gke_cluster
  location = var.gke_cluster_region
  project  = var.project_id
}
