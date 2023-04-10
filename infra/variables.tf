
# variable "terraform_service_account" {
#   description = "Service account email of the account to impersonate to run Terraform."
#   type        = string
# }


variable "project_id" {
  description = "CloudSQL project ID"
  type        = string
}


## Required by SQL
variable "shared_vpc_name" {
  description = "Name of the shared VPC"
  type        = string
}

variable "network_project_id" {
  description = "Network project ID"
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


variable "psc_address_name" {
  description = "Private service connect address name"
  type        = string

}


## Required by Workload Identity
variable "gke_cluster" {
  description = "GKE cluster name"
  type        = string
}

variable "gke_cluster_region" {
  description = "GKE cluster region"
  type        = string
}

variable "gke_namespace" {
  description = "GKE namespace name"
  type        = string
}

variable "gcp_sa" {
  description = "GCP SA name used by App"
  type        = string
}
