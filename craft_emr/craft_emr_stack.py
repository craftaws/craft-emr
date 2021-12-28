from aws_cdk import (
    Stack,
)
from constructs import Construct
from artifacts import CraftEmr

class CraftEmrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CraftEmr(self, "craft-emr")
