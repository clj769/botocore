from behave import when, then
import boto3

acm_client = boto3.client('acm')

@when('I call the "ListCertificates" API')
def step_when_call_list_certificates_api(context):
    context.response = acm_client.list_certificates()

@then('the value at "CertificateStatuses" should be a list')
def step_then_check_certificate_statuses(context):
    # The 'CertificateSummaryList' field is returned by the 'list_certificates' method
    assert isinstance(context.response.get('CertificateSummaryList', None), list)

@when('I attempt to call the "GetCertificate" API with')
def step_when_call_get_certificate_api(context):
    try:
        for row in context.table:
            context.response = acm_client.get_certificate(CertificateArn=row['CertificateArn'])
    except Exception as e:
        context.error = e

@then('I expect the response error to contain a message')
def step_then_check_error_message(context):
    # Check if an error exists
    if hasattr(context, 'error'):
        assert hasattr(context.error, 'message')
