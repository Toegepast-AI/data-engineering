terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.47.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json"
  project = "single-planet-468711-b0"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "single-planet-468711-b0"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}