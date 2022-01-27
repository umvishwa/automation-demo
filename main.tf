resource "google_storage_bucket" "bucket-cloud-demo2" {
  name = "cloud-demo-bucket-umvishwa"
  location = "us-west2"
}

resource "google_storage_bucket_object" "picture" {
  name   = "Umesh_photos.jpg"
  source = "./automation-demo/images/Umesh_photos.jpg"
  bucket = "cloud-demo-bucket-umvishwa"
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "./automation-demo/cloud-fn-demo/"
  output_path = "./automation-demo/cloud-fn-demo//cloud-fn-demo.zip"
}

resource "google_storage_bucket" "bucket" {
  name     = "temp-bucket0101"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name   = "cloud-fn-demo.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./automation-demo/cloud-fn-demo/main.py"
}

resource "google_cloudfunctions_function" "function" {
  name        = "cloud-fn-demo"
  description = "My function"
  runtime     = "nodejs14"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "helloGET"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
