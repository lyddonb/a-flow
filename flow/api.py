import logging

from collections import namedtuple

from botocore.exceptions import ClientError


RESPONSE_META_DATA = "ResponseMetadata"
HTTP_STATUS_CODE = 'HTTPStatusCode'
REQUEST_ID = "RequestId"
ERROR = 'Error'
MESSAGE = 'Message'
CODE = 'Code'

ResultType = namedtuple('ResultType', ['success', 'status_code', 'request_id',
                                       'result'])

ErrorResult = namedtuple('ErrorResult', ['message', 'code'])


# TODO: Fail the token refresh errors hard.


def make_request(func, *args, **kwargs):
    """Make an AWS request and parse the request result and return a
    ResultType namedtuple.
    """
    try:
        result = func(*args, **kwargs)
    except ClientError, ce:
        logging.debug(ce)
        response = ce.response if ce.response else {}
        error = response.pop(ERROR, {})
        error_result = ErrorResult(error.get(MESSAGE, ""), error.get(CODE, ""))
        return _build_result_type(False, response, error_result)

    return _build_result_type(True, result, result)


def _build_result_type(success, result, payload):
    status_code, request_id = _get_meta(result)

    return ResultType(success, status_code, request_id, payload)


def _get_meta(result):
    meta = result.pop(RESPONSE_META_DATA, None)

    if meta:
        return meta.get(HTTP_STATUS_CODE, 0), meta.get('RequestId', "")

    return 0, ""
