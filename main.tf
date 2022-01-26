resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-swagatika2"
  location = "us-west2"
}

module "consul" {
  source = "github.com/mvishwa/automation-demo"
}

resource "google_storage_bucket_object" "picture" {
  name   = "photos"
  source = "/images/Umesh_photos.jpg"
  bucket = "cloud-demo-bucket-swagatika2"
}
