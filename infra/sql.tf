module "mysql-db" {
  source               = "GoogleCloudPlatform/sql-db/google//modules/safer_mysql"
  name                 = "sample-app-mysql-db"
  random_instance_name = true
  project_id           = var.project_id

  deletion_protection = false

  database_version   = "MYSQL_8_0"
  region             = var.region
  zone               = var.master_instance_zone
  tier               = "db-n1-standard-1"
  assign_public_ip   = "false"
  vpc_network        = data.google_compute_network.shared-vpc.self_link
  allocated_ip_range = var.psc_address_name
  database_flags = [{
    name  = "cloudsql_iam_authentication"
    value = "On"
  }]

  additional_databases = [{
    name      = "sampleapp"
    charset   = ""
    collation = ""
  }]

  # Because Cloud IAM acts as a primary authentication and authorization mechanism,
  # we can consider MySQL usernames and passwords are a secondary access controls
  # that can be used to further restrict access for reliability or safety purposes. 
  # For example, removing the ability of modifying tables from production users 
  # that don't need such a capability. The module, by default, creates users that:
  # 1. only allow connections from host ~cloudsqlproxy to ensure that nobody can access 
  #    data without connecting via the Cloud SQL Proxy.
  # 2. have randomly generated passwords, which can be stored in configuration files. 
  #    Such passwords can be considered as secure as API Keys rather than strong credentials for access.
  # more details here: https://github.com/terraform-google-modules/terraform-google-sql-db/tree/master/modules/safer_mysql#define-mysql-users-and-passwords-on-your-instance

  #   additional_users = [
  #     {
  #       name            = "sample-app"
  #       password        = "PaSsWoRd"
  #       host            = "localhost"
  #       type            = "BUILT_IN"
  #       random_password = false
  #     },
  #   ]
}

## Service account based authentication + DB login can be used by creating users
## and then granting them permissions on table using GRANT statement
## Please check https://cloud.google.com/sql/docs/mysql/add-manage-iam-users#grant-db-privileges
resource "google_sql_user" "users" {
  name     = module.my-app-workload-identity.gcp_service_account_email
  instance = module.mysql-db.instance_name
  type     = "CLOUD_IAM_SERVICE_ACCOUNT"
  project  = var.project_id
}


# we can create one SA for admins and use that in CI/CD pipeline etc
# resource "google_sql_user" "admins" {
#   name     = module.sql-admin-workload-identity.gcp_service_account_email
#   instance = module.mysql-db.instance_name
#   type     = "CLOUD_IAM_SERVICE_ACCOUNT"
#   project  = var.project_id
# }
