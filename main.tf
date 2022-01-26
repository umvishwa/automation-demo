resource "google_storage_bucket" "bucket-cloud-demo" {
  name = "cloud-demo-bucket-swagatika"
  location = "europe-west1"
}
resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-swagatika2"
  location = "us-west2"
}
