provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "cloud-bucket-100"
    prefix = "terraform/state"
  }
}
