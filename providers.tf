provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "cloudbucket-100"
    prefix = "terraform/state"
  }
}
