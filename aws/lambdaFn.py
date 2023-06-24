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
        self.jobQueue = os.getenv("jobQueue")
        self.jobDefinition = os.getenv("jobDefinition")
        self.attemptDurationSeconds = os.getenv("attemptDurationSeconds")
 
 
class Awsbatch(AWSBatchSettings):
 
    def __init__(self):
        self.client = boto3.client("batch",
                                   aws_access_key_id=AWS_ACCESS_KEY,
                                   aws_secret_access_key=AWS_SECRET_KEY,
                                   region_name=AWS_REGION_NAME)
        AWSBatchSettings.__init__(self)
 
 
    def run(self, jobName = 'scrape job',python_file_name='pyscraper.py', payload={}):
 
        try:
            if payload == {}:
                response = self.client.submit_job(
                    jobName=jobName,
                    jobQueue=self.jobQueue,
                    jobDefinition=self.jobDefinition,
                    containerOverrides={
                        "command": ["python",
                                    python_file_name,
                                    payload
                                    ]
                    },
                    timeout={
                        'attemptDurationSeconds': int(self.attemptDurationSeconds)
                    })
                return {
                    "status":-1,
                    "data":{
                        "response":response
                    },
                    "error":{
 
                    }
                }
 
            else:
                payload = json.dumps(payload)
                response = self.client.submit_job(
                    jobName=jobName,
                    jobQueue=self.jobQueue,
                    jobDefinition=self.jobDefinition,
                    containerOverrides={
                        "command": ["python",
                                    python_file_name,
                                    payload
                                    ]
                    },
                    timeout={
                        'attemptDurationSeconds': int(self.attemptDurationSeconds)
                    })
                return {
                    "status":-1,
                    "data":{
                        "response":response
                    },
                    "error":{
 
                    }
                }
 
        except Exception as e:
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
 
 
if __name__ == "__main__":
    main()