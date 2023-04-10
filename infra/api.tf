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
