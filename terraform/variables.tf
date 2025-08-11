
variable "credentials_file" {
  description = "Path to the service account key file"
  type        = string
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "single-planet-468711-b0"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "US"
}

variable "region" {
  description = "The region of the resources"
  type        = string
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "The name of the BigQuery dataset"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "The name of the Google Cloud Storage bucket"
  type        = string
  default     = "single-planet-468711-b0"
}

variable "gcs_storage_class" {
  description = "The storage class of the Google Cloud Storage bucket"
  type        = string
  default     = "STANDARD"
}