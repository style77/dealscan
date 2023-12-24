variable "region" {
    description = "AWS server region"
    default     = "eu-central-1"
}

variable "project_name" {
    description = "Project name"
    default     = "dealscan"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]
}

# networking

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}

# load balancer

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/"
}

# ecs

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "production"
}

variable "docker_image_url_django" {
  description = "Docker image to run in the ECS cluster"
  default     = "448170394442.dkr.ecr.eu-central-1.amazonaws.com/dealscan-backend:latest"
}

variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 2
}

variable "ec2_cpu" {
  description = "Amount of CPU for EC2 instances. E.g., '256' (.25 vCPU)"
  default     = "256"  # Default value for EC2 CPU
}

variable "ec2_memory" {
  description = "Amount of memory for EC2 instances. E.g., '512' (0.5GB)"
  default     = "512"  # Default value for EC2 memory
}

# rds

variable "rds_db_name" {
  description = "RDS database name"
  default     = "dealscan"
}
variable "rds_username" {
  description = "RDS database username"
  default     = "postgres"
}
variable "rds_password" {
  description = "RDS database password"
}
variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t3.micro"
}

# logs

variable "log_retention_in_days" {
  default = 30
}

# Dealscan settings

variable "demo" {
  description = "Demo"
  type        = bool
}

variable "secret_key" {
  description = "Secret key"
}

variable "stripe_publishable_key" {
  description = "Stripe publishable key"
}

variable "stripe_live_secret_key" {
  description = "Stripe live secret key"  
}
