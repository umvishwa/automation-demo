resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-umvishwa"
  location = "us-west2"
}

resource "google_storage_bucket_object" "picture" {
  name   = "Umesh_photos.jpg"
  source = "/home/runner/work/automation-demo/automation-demo/images/Umesh_photos.jpg"
  bucket = "cloud-demo-bucket-umvishwa"
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "/home/runner/work/automation-demo/automation-demo/cloud-fn-demo/"
  output_path = "/home/runner/work/automation-demo/automation-demo/cloud-fn-demo//cloud-fn-demo.zip"
}

resource "google_storage_bucket" "bucket" {
  name     = "temp-bucket0101"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name   = "cloud-fn-demo.zip"
  bucket = google_storage_bucket.bucket.name
  source = "/home/runner/work/automation-demo/automation-demo/cloud-fn-demo/main.py"
}

resource "google_cloudfunctions_function" "function" {
  name        = "cloud-fn-demo"
  description = "My function"
  runtime     = "python39"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "hello_world"
}
