provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "cloud-demo-bucket-umvishwa"
    prefix = "terraform/state"
  }
}
