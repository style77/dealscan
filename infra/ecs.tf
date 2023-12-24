resource "aws_ecs_cluster" "production" {
  name = "${var.ecs_cluster_name}-cluster"
}

data "template_file" "app" {
  template = file("templates/django_app.json.tpl")

  vars = {
    docker_image_url_django = var.docker_image_url_django
    region                  = var.region
    rds_db_name             = var.rds_db_name
    rds_username            = var.rds_username
    rds_password            = var.rds_password
    rds_hostname            = aws_db_instance.production.address
    demo                    = var.demo
    secret_key              = var.secret_key
    stripe_publishable_key  = var.stripe_publishable_key
    stripe_live_secret_key  = var.stripe_live_secret_key
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "dealscan"
  network_mode             = "bridge"  # Use "bridge" for EC2
  requires_compatibilities = ["EC2"]   # Set compatibility to EC2
  cpu                      = "${var.ec2_cpu}"
  memory                   = "${var.ec2_memory}"
  execution_role_arn       = aws_iam_role.ecs-task-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-execution-role.arn
  container_definitions    = data.template_file.app.rendered
  depends_on               = [aws_db_instance.production]
}

resource "aws_ecs_task_definition" "django_migration" {
  family                = "django-migration-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["EC2"]
  cpu                   = var.ec2_cpu
  memory                = var.ec2_memory
  execution_role_arn    = aws_iam_role.ecs-task-execution-role.arn

  container_definitions = jsonencode([
    {
      name  = "django-migration-container"
      image = var.docker_image_url_django
      environment: [
        {
            "name": "RDS_DB_NAME",
            "value": var.rds_db_name
        },
        {
            "name": "RDS_USERNAME",
            "value": var.rds_username
        },
        {
            "name": "RDS_PASSWORD",
            "value": var.rds_password
        },
        {
            "name": "RDS_HOSTNAME",
            "value": aws_db_instance.production.address
        },
        {
            "name": "RDS_PORT",
            "value": "5432"
        }
      ],
      # Run migrations as the command
      command = ["python", "manage.py", "migrate"]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/dealscan"
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }

      portMappings = [
        {
          containerPort = 8000
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "production" {
  # Existing configurations remain unchanged except for "launch_type" and "network_configuration"
  name            = "${var.ecs_cluster_name}-service"
  cluster         = aws_ecs_cluster.production.id
  task_definition = aws_ecs_task_definition.app.arn
  launch_type     = "EC2"  # Change to EC2

  # Adjust network configuration for EC2 launch type (use appropriate subnets and security groups)
  network_configuration {
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]  # Use appropriate private subnets
    security_groups  = [aws_security_group.ecs-ec2.id]  # Use appropriate security groups for EC2
    assign_public_ip = false  # EC2 instances in private subnets don't need public IPs
  }

  # Load balancer settings remain the same
  load_balancer {
    target_group_arn = aws_alb_target_group.default-target-group.arn
    container_name   = "dealscan"
    container_port   = 8000
  }
}