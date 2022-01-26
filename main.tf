resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-swagatika2"
  location = "us-west2"
}
data "google_storage_bucket_object" "file" {
  name   = "images/Umesh_photos.jpg"
  bucket = "cloud-demo-bucket-swagatika2"
}
