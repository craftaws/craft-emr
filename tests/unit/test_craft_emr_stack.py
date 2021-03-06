import aws_cdk as cdk
import aws_cdk.assertions as assertions
from constructs import Construct

from craft_emr.craft_emr_stack import CraftEmrStack

# example tests. To run these tests, uncomment this file along with the example
# resource in craft_emr/craft_emr_stack.py
def test_sqs_queue_created():
    app = cdk.App()
    stack = CraftEmrStack(app, "craft-emr")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
