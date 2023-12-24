resource "aws_cloudwatch_log_group" "django-log-group" {
  name              = "/ecs/dealscan"
  retention_in_days = var.log_retention_in_days
}