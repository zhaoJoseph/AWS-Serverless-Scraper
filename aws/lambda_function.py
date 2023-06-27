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
 
    def __init__(self, object):
        self.jobQueue = object["jobQueue"]
        self.jobDefinition = object["jobDefinition"]
        self.urlArray = object["URL_ARRAY"]
 
 
class Awsbatch(AWSBatchSettings):
 
    def __init__(self, event):
        self.client = boto3.client("batch",
                                   aws_access_key_id=AWS_ACCESS_KEY,
                                   aws_secret_access_key=AWS_SECRET_KEY,
                                   region_name=AWS_REGION_NAME)
        AWSBatchSettings.__init__(self, event)
 
 
    def run(self, jobName = 'scrape-job'):
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
                            'value': str(self.urlArray)
                        },
                    ],
                }
                )

            print(response, "RESPONSE")
            
            return {
                "status":200,
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
 
 
def lambda_handler(event, context):
 
    Awsbatch_helper = Awsbatch(event)
    Awsbatch_helper.run()
 

# For dev environment
if __name__ == '__main__':
    event = {"jobQueue" : "scraper_queue", "jobDefinition" : "scraper_definition", "URL_ARRAY" : ["https://www.amazon.ca/gp/goldbox"]}
    context = []
    lambda_handler(event, context)