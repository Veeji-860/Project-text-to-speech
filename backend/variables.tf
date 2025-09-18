variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "txt_2_speech_audio_bucket" {
  description = "S3 bucket name for storing audio files"
  type        = string
  default     = "text-to-speech-audio-bucket10"
}

variable "txt_2_speech_frontend_bucket" {
  description = "S3 bucket name for hosting static website"
  type        = string
  default     = "static-website-bucket10"
}

variable "txt_2_speech_lambda_function" {
  description = "Name of the Lambda function"
  type        = string
  default     = "text-to-speech"
}

variable "txt_2_speech_api_gateway" {
  description = "Name of the API Gateway"
  type        = string
  default     = "text-to-speech-api"
}

variable "txt_2_speech_lambda_execution_role" {
  description = "Name of the Lambda execution role"
  type        = string
  default     = "text-to-speech-execution-role"
}

variable "txt_2_speech_lambda_policy" {
  description = "Name of the Lambda policy"
  type        = string
  default     = "text-to-speech-policy"
}