[
  {
    "name": "dealscan",
    "image": "${docker_image_url_django}",
    "essential": true,
    "cpu": 10,
    "memory": 512,
    "portMappings": [
      {
        "containerPort": 8000,
        "protocol": "tcp"
      }
    ],
    "command": ["gunicorn", "-b", "0.0.0.0:8000", "dealscan.wsgi:application"],
    "environment": [
      {
        "name": "DJANGO_SETTINGS_MODULE",
        "value": "dealscan.settings"
      },
      {
        "name": "DEBUG",
        "value": "False"
      },
      {
        "name": "ENVIRONMENT",
        "value": "prod"
      },
      {
        "name": "DATABASE_URL",
        "value": "postgres://${rds_username}:${rds_password}@${rds_hostname}:5432/${rds_db_name}"
      },
      {
        "name": "DEMO",
        "value": "${demo}"
      },
      {
        "name": "STRIPE_PUBLISHABLE_KEY",
        "value": "${stripe_publishable_key}"
      },
      {
        "name": "STRIPE_LIVE_SECRET_KEY",
        "value": "${stripe_live_secret_key}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/dealscan",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "dealscan-log-stream"
      }
    }
  }
]