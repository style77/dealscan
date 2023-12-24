import boto3
import click


def get_current_task_definition(client, cluster, service):
    response = client.describe_services(cluster=cluster, services=[service])
    current_task_arn = response["services"][0]["taskDefinition"]
    return client.describe_task_definition(taskDefinition=current_task_arn)


@click.command()
@click.option("--cluster", help="Name of the ECS cluster", required=True)
@click.option("--service", help="Name of the ECS service", required=True)
@click.option(
    "--image", help="Docker image URL for the updated application", required=True
)
def deploy(cluster, service, image):
    client = boto3.client("ecs")

    print("Fetching current task definition...")
    response = get_current_task_definition(client, cluster, service)
    container_definition = response["taskDefinition"]["containerDefinitions"][0].copy()

    container_definition["image"] = image
    print(f"Updated image to: {image}")

    print("Registering new task definition...")
    response = client.register_task_definition(
        family=response["taskDefinition"]["family"],
        volumes=response["taskDefinition"]["volumes"],
        containerDefinitions=[container_definition],
        cpu="256",
        memory="512",
        networkMode="awsvpc",
        requiresCompatibilities=["EC2"],
        executionRoleArn="ecs_task_execution_role_prod",
        taskRoleArn="ecs_task_execution_role_prod",
    )
    new_task_arn = response["taskDefinition"]["taskDefinitionArn"]
    print(f"New task definition ARN: {new_task_arn}")

    print("Updating ECS service with new task definition...")
    client.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=new_task_arn,
    )
    print("Service updated!")


if __name__ == "__main__":
    deploy()
