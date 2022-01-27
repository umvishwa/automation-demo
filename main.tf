/*resource "google_storage_bucket" "bucket" {
  name     = "cibuild1-bucket-100"
  location = "europe-west1"
}

resource "google_storage_bucket_object" "archive" {
  name   = "Umesh_photos.jpg"
  bucket = google_storage_bucket.bucket.name
  source = "/home/runner/work/automation-demo/automation-demo/images/Umesh_photos.jpg"
}
*/

 resource "google_storage_bucket" "bucket" {
  name     = "temp-bucket0101569"
  location = "europe-west2"
}

resource "google_storage_bucket_object" "archive" {
  name   = "Archive.zip"
  bucket = google_storage_bucket.bucket.name
  source = "/home/runner/work/automation-demo/automation-demo/cloud-fn-demo/Archive.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "fn-cloud-demo"
  description = "My function"
  runtime     = "python37"
  available_memory_mb   = 128
  build_environment_variables = {GOOGLE_FUNCTION_SOURCE:Archive/main.py}
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "hello_world"
}

