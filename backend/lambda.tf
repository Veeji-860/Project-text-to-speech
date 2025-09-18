resource "aws_lambda_function" "text_to_speech" {
  function_name = var.txt_2_speech_lambda_function
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256
  reserved_concurrent_executions = 10

  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")

  environment {
    variables = {
      AUDIO_BUCKET     = aws_s3_bucket.audio.bucket
      MAX_TEXT_LENGTH  = "3000"
    }
  }

  dead_letter_config {
    target_arn = aws_sqs_queue.dlq.arn
  }
}

# Dead letter queue for failed invocations
resource "aws_sqs_queue" "dlq" {
  name = "${var.txt_2_speech_lambda_function}-dlq"
  message_retention_seconds = 1209600 # 14 days
}