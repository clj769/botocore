from behave import when, then
import boto3
import botocore.exceptions

autoscaling_client = boto3.client('autoscaling')

@when('I call the "DescribeScalingProcessTypes" API')
def step_when_call_describe_scaling_process_types_api(context):
    context.response = autoscaling_client.describe_scaling_process_types()

@then('the value at "Processes" should be a list')
def step_then_check_processes(context):
    assert isinstance(context.response.get('Processes', None), list)

@when('I attempt to call the "CreateLaunchConfiguration" API with')
def step_when_call_create_launch_configuration_api(context):
    try:
        for row in context.table:
            # Get the columns from the row headings
            params = {heading: row[heading] for heading in context.table.headings}
            context.response = autoscaling_client.create_launch_configuration(**params)
    except botocore.exceptions.BotoCoreError as e:
        context.error = e

@then('I expect the response error code to be "ValidationError"')
def step_then_check_error_code(context):
    if hasattr(context, 'error'):
        assert isinstance(context.error, botocore.exceptions.ClientError)
        assert context.error.response['Error']['Code'] == "ValidationError"

@then('I expect the response error to contain a message')
def step_then_check_error_message(context):
    if hasattr(context, 'error'):
        assert 'message' in context.error.response['Error']

