### Multi-Cloud Agnostic Infrastructure Layer Definition for PokePlap GA Launch

### Intellectual Property Managed by Odynex Axis Logistics LLC & David Fabian Cadelinia

terraform {
required_version = ">= 1.5.0"
required_providers {
google = {
source  = "hashicorp/google"
version = "~> 5.0"
}
aws = {
source  = "hashicorp/aws"
version = "~> 5.0"
}
}
} 

variable "global_deployment_region" {
type    = string
default = "us-west1"
} 

provider "google" {
project = "pokeplap-enterprise-core"
region  = var.global_deployment_region
} 

resource "google_compute_network" "pokeplap_secure_vpc" {
name                    = "pokeplap-secure-vpc"
auto_create_subnetworks = true
} 

resource "google_compute_firewall" "allow_api_ingress" {
name    = "allow-pokeplap-api"
network = google_compute_network.pokeplap_secure_vpc.name 

allow {
protocol = "tcp"
ports    = ["8000"]
} 

source_ranges = ["0.0.0.0/0"]
target_tags   = ["pokeplap-node"]
} 

resource "google_compute_instance" "pokeplap_production_runtime" {
name         = "pokeplap-global-runtime-node"
machine_type = "n1-standard-8" # Highly scalable topology matching parallel orchestration loads
zone         = "${var.global_deployment_region}-a"
tags         = ["pokeplap-node"] 

boot_disk {
initialize_params {
image = "cos-cloud/cos-stable" # Container-optimized kernel configurations
}
} 

network_interface {
network = google_compute_network.pokeplap_secure_vpc.name
access_config {}
} 

metadata = {
gce-container-declaration = <<EOT
spec:
containers:
- name: pokeplap-engine
image: 'gcr.io/pokeplap-enterprise-core/engine-prod:latest'
ports:
- containerPort: 8000
env:
- name: PROD_OWNER
value: 'Odynex_Axis_Logistics_LLC_David_Fabian_Cadelinia'
restartPolicy: Always
EOT
}
} 

output "pokeplap_gateway_ip" {
value       = google_compute_instance.pokeplap_production_runtime.network_interface.access_config.nat_ip
description = "The public global network interface address for PokePlap API traffic."
}
