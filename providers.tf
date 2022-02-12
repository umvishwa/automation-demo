provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "local" {
    path:'./terraform/state'
    #bucket = "cloud-bucket-100"
    #prefix = "terraform/state"
  }
}
