#!/usr/bin/env python3
import aws_cdk as cdk
from cloud_computing_assignment3.cloud_computing_assignment3_stack import CloudComputingAssignment3Stack
from cloud_computing_assignment3.driver_lambda_stack import DriverLambdaStack
from cloud_computing_assignment3.plotting_lambda_stack import PlottingLambdaStack
from cloud_computing_assignment3.size_tracking_lambda_stack import SizeTrackingLambdaStack
from cloud_computing_assignment3.logging_lambda_stack import LoggingLambdaStack
from cloud_computing_assignment3.cleaner_lambda_stack import CleanerLambdaStack

app = cdk.App()

# Define each Lambda in its own stack



# Deploy the main infrastructure stack
infrastructure_stack = CloudComputingAssignment3Stack(app, "CloudComputingAssignment3Stack")

# Deploy the size tracking Lambda stack
lambda_stack = SizeTrackingLambdaStack(app, "SizeTrackingLambdaStack")

# Deploy the logging stack
LoggingLambdaStack(app, "LoggingLambdaStack")

CleanerLambdaStack(app, "CleanerLambdaStack")

PlottingLambdaStack(app, "PlottingLambdaStack")

DriverLambdaStack(app, "DriverLambdaStack")


app.synth()
