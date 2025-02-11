import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_computing_assignment3.cloud_computing_assignment3_stack import CloudComputingAssignment3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_computing_assignment3/cloud_computing_assignment3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudComputingAssignment3Stack(app, "cloud-computing-assignment3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
