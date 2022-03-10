# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.65"
    }
  }

  required_version = ">= 0.12"
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id = var.tenant_id
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location_name
}

# Create a virtual network within the resource group
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location_name
  address_space       = ["10.0.0.0/16"]
  depends_on = [
  azurerm_resource_group.rg,
  ]
}
# Create subnet 1
resource "azurerm_subnet" "subnet" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
  delegation {
    name = "fs"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

# Create subnet 2
resource "azurerm_subnet" "subnet2" {
  name                 = var.subnet_name2
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]

}
# Create public ip
resource "azurerm_public_ip" "public_ip" {
  name                = "vm_public_ip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location_name
  allocation_method   = "Dynamic"
  
}

# Create network interface & config public ip
resource "azurerm_network_interface" "main" {
  name                = "testinetworkinterface"
  location            = var.location_name
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = azurerm_subnet.subnet2.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

resource "azurerm_private_dns_zone" "example" {
  name                = "project4.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "example" {
  name                  = "project4.com"
  private_dns_zone_name = azurerm_private_dns_zone.example.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  resource_group_name   = azurerm_resource_group.rg.name
}

# Create SQL server
resource "azurerm_postgresql_flexible_server" "SQL" {
  name                   = var.vm_server_name
  resource_group_name    = azurerm_resource_group.rg.name
  location               = var.location_name
  version                = "12"
  delegated_subnet_id    = azurerm_subnet.subnet.id
  private_dns_zone_id    = azurerm_private_dns_zone.example.id
  administrator_login    = var.tunnus
  administrator_password = var.salasana
  zone                   = "1"

  storage_mb = 32768

  sku_name   = "B_Standard_B1ms"
  depends_on = [azurerm_private_dns_zone_virtual_network_link.example]

}

# Create VM workstation from image
resource "azurerm_virtual_machine" "vm" {
  name                  = var.vm_desktop_name
  location              = var.location_name
  resource_group_name   = azurerm_resource_group.rg.name
  vm_size               = "Standard_F1"
  network_interface_ids = [azurerm_network_interface.main.id]

  storage_image_reference {
    id = var.image_id
  }

  storage_os_disk {
    name          = "osdisk1"
    caching       = "ReadWrite"
    create_option = "FromImage"
  }

  os_profile {
    computer_name  = var.vm_desktop_name
    admin_username = var.tunnusvm
    admin_password = var.salasanavm
  }

  os_profile_windows_config {
  }
}

# Create NSG
resource "azurerm_network_security_group" "example" {
  name                = "NSGforVMdesktop"
  location            = var.location_name
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "Allow RDP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "3389"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Associate NSG with network interface
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.example.id
}
