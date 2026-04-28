provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "devprod" {
  name     = "rg-${var.project_name}-devprod-${var.environment}"
  location = var.location
}

# --- Productivity Analytics Hub (AKS) ---

resource "azurerm_kubernetes_cluster" "devprod_k8s" {
  name                = "aks-devprod-iq-${var.environment}"
  location            = azurerm_resource_group.devprod.location
  resource_group_name = azurerm_resource_group.devprod.name
  dns_prefix          = "devprod-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Effectiveness Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-devprod-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.devprod.name
  location               = azurerm_resource_group.devprod.location
  version                = "13"
  administrator_login    = "devprodadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Search & Discovery Hub (Azure Search) ---

resource "azurerm_search_service" "discovery" {
  name                = "search-devprod-discovery-${var.environment}"
  resource_group_name = azurerm_resource_group.devprod.name
  location            = azurerm_resource_group.devprod.location
  sku                 = "standard"
}

# --- Multi-Cloud Persistence (AWS S3 Telemetry Sink) ---

resource "aws_s3_bucket" "telemetry" {
  bucket = "db-devprod-telemetry-sink-${var.environment}"
}
