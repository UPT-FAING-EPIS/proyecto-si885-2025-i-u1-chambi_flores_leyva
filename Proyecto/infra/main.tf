provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

# Grupo de recursos para SoftRepoTrack
resource "azurerm_resource_group" "softrepotrack_rg" {
  name     = "rg-softrepotrack"
  location = "West US 2"
}

# Servidor MSSQL para SoftRepoTrack
resource "azurerm_mssql_server" "softrepotrack_sql_server" {
  name                         = "sqlserversoftrepotrack"
  resource_group_name          = azurerm_resource_group.softrepotrack_rg.name
  location                     = azurerm_resource_group.softrepotrack_rg.location
  version                      = "12.0"
  administrator_login          = var.sqladmin_username
  administrator_login_password = var.sqladmin_password

  identity {
    type = "SystemAssigned"
  }
}

# Base de datos SQL para el análisis de datos
resource "azurerm_mssql_database" "softrepotrack_database" {
  name                        = "bdsoftrepotrack"
  server_id                   = azurerm_mssql_server.softrepotrack_sql_server.id
  sku_name                    = "GP_S_Gen5_2"
  collation                   = "SQL_Latin1_General_CP1_CI_AS"
  auto_pause_delay_in_minutes = 60
  min_capacity                = 0.5
  storage_account_type        = "Local"
}

# Regla de firewall para permitir acceso desde cualquier IP
resource "azurerm_mssql_firewall_rule" "allow_all_ips" {
  name             = "AllowAllIPs"
  server_id        = azurerm_mssql_server.softrepotrack_sql_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}
