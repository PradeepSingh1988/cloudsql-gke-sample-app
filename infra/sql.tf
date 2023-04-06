

resource "google_project_service" "cloud_sql_service" {
  project                    = var.project_id
  service                    = "sqladmin.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

resource "google_project_service" "service_networking_api" {
  project                    = var.project_id
  service                    = "servicenetworking.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}


module "sql-db" {
  source               = "GoogleCloudPlatform/sql-db/google//modules/postgresql"
  name                 = "postgresql-ha-instance"
  random_instance_name = true
  project_id           = var.project_id

  # Master Configuration
  database_version    = "POSTGRES_14"
  region              = var.region
  tier                = "db-custom-1-3840"
  zone                = var.master_instance_zone
  availability_type   = "REGIONAL"
  deletion_protection = false
  user_labels = {
    environment = "dev"
  }

  ip_configuration = {
    ipv4_enabled                                  = false
    require_ssl                                   = true
    private_network                               = data.google_compute_network.shared-vpc.self_link
    allocated_ip_range                            = var.psc_address_name
    authorized_networks                           = []
    enable_private_path_for_google_cloud_services = true
  }
  database_flags = [
    {
      name  = "cloudsql.iam_authentication"
      value = "on"
    },
  ]

  // Read replica configurations
  read_replica_name_suffix = "-replica"
  read_replicas = [
    {
      name              = "0"
      zone              = var.replica_instance_zone
      availability_type = "REGIONAL"
      tier              = "db-custom-1-3840"
      ip_configuration = {
        ipv4_enabled                                  = false
        require_ssl                                   = true
        private_network                               = data.google_compute_network.shared-vpc.self_link
        allocated_ip_range                            = var.psc_address_name
        authorized_networks                           = []
        enable_private_path_for_google_cloud_services = true
      }
      database_flags = [
        {
          name  = "cloudsql.iam_authentication"
          value = "on"
        },
      ]
      disk_autoresize       = null
      disk_autoresize_limit = null
      disk_size             = null
      disk_type             = "PD_HDD"
      user_labels           = { environment = "dev" }
      encryption_key_name   = null
    }
  ]

  additional_databases = [
    {
      name      = "sample-app"
      charset   = "UTF8"
      collation = "en_US.UTF8"
    },
  ]
  module_depends_on = [google_project_service.cloud_sql_service]
}
