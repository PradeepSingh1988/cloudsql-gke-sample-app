
variable "terraform_service_account" {
  description = "Service account email of the account to impersonate to run Terraform."
  type        = string
}

variable "shared_vpc_name" {
  description = "Name of the shared VPC"
  type        = string
}

variable "subnet" {
  description = "Name of the subnet used for GKE  nodes"
  type        = string
}

variable "pods_range" {
  description = "Name of the pod range for GKE pods"
  type        = string
}

variable "services_range" {
  description = "Name of the Services range for GKE pods"
  type        = string
}

variable "gke_node_service_account" {
  description = "GKE node service account name"
  type        = string
}

variable "network_project_id" {
  description = "Network project ID"
  type        = string
}


variable "project_id" {
  description = "CloudSQL project ID"
  type        = string
}

variable "region" {
  description = "region"
  type        = string
}

variable "master_instance_zone" {
  description = "Master Zone"
  type        = string
}


variable "replica_instance_zone" {
  description = "Master Zone"
  type        = string
}

variable "psc_address_name" {
  description = "Private service connect address name"
  type        = string

}

variable "gke_cluster" {
  description = "GKE cluster name"
  type        = string
}

variable "gke_cluster_region" {
  description = "GKE cluster region"
  type        = string
}

