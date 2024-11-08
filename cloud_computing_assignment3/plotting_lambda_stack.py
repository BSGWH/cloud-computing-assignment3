from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
)
from constructs import Construct


class PlottingLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the existing DynamoDB table
        dynamodb_table = dynamodb.Table.from_table_name(
            self,
            "ImportedDynamoDBTable",
            table_name="cdk-S3-object-size-history"
        )

        # Import the existing S3 bucket
        s3_bucket = s3.Bucket.from_bucket_name(
            self,
            "ImportedS3Bucket",
            bucket_name="weihao-cdk-bucket"
        )

        # Define Matplotlib Layer
        matplotlib_layer = _lambda.LayerVersion(
            self,
            "MatplotlibLayer",
            code=_lambda.Code.from_asset("matplotlib_layer.zip"),  # Ensure this path points to the correct zip file
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="A layer with matplotlib dependencies"
        )

        # Define the Plotting Lambda function with the layer
        plotting_lambda = _lambda.Function(
            self,
            "PlottingLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="plotting_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda/plotting_lambda"),  # Folder containing Lambda code
            layers=[matplotlib_layer],  # Attach the layer
            environment={
                "DYNAMODB_TABLE_NAME": dynamodb_table.table_name,
                "S3_BUCKET_NAME": s3_bucket.bucket_name
            },
            timeout=Duration.minutes(1)
        )

        # Define and attach full access policies for S3 and DynamoDB
        full_s3_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        full_dynamodb_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")

        plotting_lambda.role.add_managed_policy(full_s3_policy)
        plotting_lambda.role.add_managed_policy(full_dynamodb_policy)

        # Set up API Gateway and link it to the plotting Lambda
        api = apigateway.LambdaRestApi(
            self,
            "PlottingApi",
            handler=plotting_lambda,
            proxy=False,
            rest_api_name="Plotting Service API",
            description="API Gateway to trigger the Plotting Lambda"
        )

        # Define a GET endpoint
        plotting_integration = apigateway.LambdaIntegration(plotting_lambda)
        api.root.add_method("GET", plotting_integration)

        # Output the API endpoint URL
        self.api_url_output = api.url
        print(f"API Gateway URL: {api.url}")
