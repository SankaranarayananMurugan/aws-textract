from typing import Text
import boto3
import time
from botocore.config import Config
from ezrest.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class Textract():
    @staticmethod
    def analyse_document(document_name):
        config = Config(region_name = 'us-east-1')

        client = boto3.client('textract',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=config
        )

        document = {
            "S3Object": {
                "Bucket": "inbox-ezcloud123",
                "Name": "invoice-samples/" + document_name
            }
        }

        response = client.start_document_analysis(DocumentLocation=document, FeatureTypes=['FORMS'])
        Textract.wait_till_job_completes(client, response.get('JobId'))

        next_token = None
        doc_analysis_results = []
        while True:
            doc_analysis_result = Textract.get_document_analysis(client, response.get('JobId'), next_token)
            doc_analysis_results.append(doc_analysis_result)

            if 'NextToken' in doc_analysis_result:
                next_token = doc_analysis_result.get('NextToken')
                print(next_token)
            else:
                break

        return doc_analysis_results

    @staticmethod
    def wait_till_job_completes(client, job_id):
        while True:
            time.sleep(5)
            doc_analysis_result = client.get_document_analysis(JobId = job_id)
            print(doc_analysis_result.get('JobStatus'))
            
            if doc_analysis_result.get('JobStatus') != 'IN_PROGRESS':
                return True

    @staticmethod
    def get_document_analysis(client, job_id, next_token):
        max_results = 1000
        if next_token is None:
            return client.get_document_analysis(
                JobId = job_id,
                MaxResults = max_results
            )
        else:
            return client.get_document_analysis(
                JobId = job_id,
                MaxResults = max_results,
                NextToken = next_token
            )
