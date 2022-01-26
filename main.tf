resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-swagatika2"
  location = "us-west2"
}
resource "google_storage_bucket_object" "textfile" {
  name   = "textfile"
  source = "../images/file.txt"
  bucket = "cloud-demo-bucket-swagatika2"
}
