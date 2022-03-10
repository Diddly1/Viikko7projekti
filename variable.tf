variable "subscription_id" { }
variable "tenant_id" { }
variable "salasana" { }
variable "tunnus" { }
variable "tunnusvm" { }
variable "salasanavm" { }
variable "image_id" { }

variable "resource_group_name" {
  default = "project_r4"
}
variable "vnet_name" {
  default = "project-vnet1"
}
variable "subnet_name" {
  default = "project-subnet1"
}
variable "subnet_name2" {
  default = "project-subnet2"
}
variable "location_name" {
  default = "westeurope"
}
variable "vm_desktop_name" {
  default = "desktop1"
}
variable "vm_server_name" {
  default = "sql1"
}
