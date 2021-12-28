'''
CDK constructs
https://docs.aws.amazon.com/ko_kr/cdk/v2/guide/constructs.html
'''
from constructs import Construct
from aws_cdk import(
    RemovalPolicy,
    aws_emr,
    aws_s3,
    aws_s3_deployment
)

class CraftEmr(Construct):
    '''Custom L2 construct to build EMR with bootstraping.

    to be installed AWS Systems Manager agent
    '''

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        bootstrap_bucket = aws_s3.Bucket(self, "craft-emr-bootstrap",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        aws_s3_deployment.BucketDeployment(self, "craft-emr-bootstrap-assets",
            sources=[aws_s3_deployment.Source.asset("./assets/emr_bootstrap")],
            destination_bucket=bootstrap_bucket
        )

        instance_config = aws_emr.CfnCluster.JobFlowInstancesConfigProperty(
            core_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
                instance_count=1,
                instance_type="m6g.xlarge"
            ),
            master_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
                instance_count=1,
                instance_type="m6g.xlarge"
            ),
        )

        bootstrap_action = aws_emr.CfnCluster.BootstrapActionConfigProperty(
            name='ssm', 
            script_bootstrap_action=aws_emr.CfnCluster.ScriptBootstrapActionConfigProperty(path=f's3://{bootstrap_bucket.bucket_name}/ssm_install.sh') 
        )

        aws_emr.CfnCluster(self, "craft-emr",
            name="emr-presto",
            release_label="emr-6.3.0",
            applications=[
                aws_emr.CfnCluster.ApplicationProperty(name="Hadoop"),
                aws_emr.CfnCluster.ApplicationProperty(name="Hive"),
                aws_emr.CfnCluster.ApplicationProperty(name="Pig"),
                aws_emr.CfnCluster.ApplicationProperty(name="Hue"),
                aws_emr.CfnCluster.ApplicationProperty(name="Presto")
            ],
            instances=instance_config,
            job_flow_role='TEST-EMR-EC2',
            service_role="EMR_DefaultRole",
            visible_to_all_users=True,
            bootstrap_actions=[bootstrap_action]
        )
