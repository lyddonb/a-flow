import boto3

SWF = boto3.client('swf')


def check_and_add_kwargs(aws_prop, value, conversion, kwargs_dict):
    if value:
        kwargs_dict[aws_prop] = conversion(value) if conversion else value

    return kwargs_dict
