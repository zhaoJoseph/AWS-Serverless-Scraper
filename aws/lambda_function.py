"""boto3 create batch job from cloudwatch event trigger"""
try:
    import os
    import boto3
    import uuid
    import json
 
except Exception as e:
    raise ("Missing  imports : {} ".format(e))
 
 
 
# ------------------------------------Settings ---------------------------------------
 
global AWS_ACCESS_KEY
global AWS_SECRET_KEY
global AWS_REGION_NAME
 
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", None)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", None)
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", None)
 
# ====================================================================================
 
 
class AWSBatchSettings(object):
 
    def __init__(self):
        print(os.getenv("jobQueue"))
        self.jobQueue = os.getenv("jobQueue")
        self.jobDefinition = os.getenv("jobDefinition")
        self.urlArray = os.getenv("URL_ARRAY")
 
 
class Awsbatch(AWSBatchSettings):
 
    def __init__(self):
        self.client = boto3.client("batch",
                                   aws_access_key_id=AWS_ACCESS_KEY,
                                   aws_secret_access_key=AWS_SECRET_KEY,
                                   region_name=AWS_REGION_NAME)
        AWSBatchSettings.__init__(self)
 
 
    def run(self, jobName = 'scrape job'):
        try:
            response = self.client.submit_job(
                jobName=jobName,
                jobQueue=self.jobQueue,
                jobDefinition=self.jobDefinition,
                arrayProperties={
                    "size": len(self.urlArray)
                },
                containerOverrides={
                    'environment': [
                        {
                            'name': 'URL_ARRAY',
                            'value': self.urlArray
                        },
                    ],
                }
                )

            print(response, "RESPONSE")
            
            return {
                "status":-1,
                "data":{
                    "response":response
                },
                "error":{

                }
            }
 
        except Exception as e:

            print(e, "EXCEPTION")

            return {
                "status":-1,
                "data":{},
                "error":{
                    "message":str(e)
                }
            }
 
 
def main():
 
    Awsbatch_helper = Awsbatch()
    Awsbatch_helper.run()
 
 
def lambda_handler(event, context):
    main()