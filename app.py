#!/usr/bin/env python3

from aws_cdk import App
from craft_emr.craft_emr_stack import CraftEmrStack

app = App()
CraftEmrStack(app, "CraftEmrStack")

app.synth()
