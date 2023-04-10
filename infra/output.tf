output "safer_mysql_user_pass" {
    value = module.mysql-db.generated_user_password
    sensitive = true
}