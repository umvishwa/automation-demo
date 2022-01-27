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
  name        = "cloud-fn-demo"
  description = "My function"
  runtime     = "python38"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "hello_world"
}
# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
