resource "google_storage_bucket" "bucket-cloud-demo" {
  name = "cloud-demo-bucket-swagatika"
  location = "europe-west1"
  force_destroy = true
}
resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-swagatika2"
  location = "us-west2"
}
resource "google_storage_bucket_object" "picture" {
  name   = "images"
  source = "/images/umesh_photos.jpg"
  bucket = "cloud-demo-bucket-swagatika2"
}
