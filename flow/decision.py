from boto.swf.layer1_decisions import Layer1Decisions

from flow.api import make_request

from flow.core import SWF
from flow.core import check_and_add_kwargs


def poll_for_decision_task(domain, task_list, identity=None,
                           next_page_token=None, maximum_page_size=1000,
                           reverse_order=False):
    """Used by deciders to get a DecisionTask from the specified decision
    taskList . A decision task may be returned for any open workflow execution
    that is using the specified task list. The task includes a paginated view of
    the history of the workflow execution. The decider should use the workflow
    type and the history to determine how to properly handle the task.

    This action initiates a long poll, where the service holds the HTTP
    connection open and responds as soon a task becomes available. If no
    decision task is available in the specified task list before the timeout of
    60 seconds expires, an empty result is returned. An empty result, in this
    context, means that a DecisionTask is returned, but that the value of
    task_token is an empty string.

    http://boto3.readthedocs.org/en/latest/reference/services/swf.html#SWF.Client.poll_for_decision_task

    domain (string) -- [REQUIRED]
    The name of the domain containing the task lists to poll.

    task_list (dict) -- [REQUIRED]
    Specifies the task list to poll for decision tasks.

        ITEMS:
            name (string) -- [REQUIRED]
            The name of the task list.

    identity (string) -- Identity of the decider making the request, which is
    recorded in the DecisionTaskStarted event in the workflow history. This
    enables diagnostic tracing when problems arise. The form of this identity is
    user defined.

    next_page_token (string) --
    If a NextPageToken was returned by a previous call, there are more results
    available. To retrieve the next page of results, make the call again using
    the returned token in nextPageToken . Keep all other arguments unchanged.

    maximum_page_size (integer) --
    The maximum number of results that will be returned per call. nextPageToken
    can be used to obtain futher pages of results. The default is 1000, which is
    the maximum allowed page size. You can, however, specify a page size smaller
    than the maximum.

    reverse_order (boolean) --
    When set to true , returns the events in reverse order. By default the
    results are returned in ascending order of the eventTimestamp of the events.

    returns dict
    """
    kwargs = {}

    for aws_prop, value, conversion in (
        ('identity', identity, None),
        ('maximumPageSize', maximum_page_size, None),
        ('reverseOrder', reverse_order, None),
        ('nextPageToken', next_page_token, None)):

        kwargs = check_and_add_kwargs(aws_prop, value, conversion, kwargs)

    result = make_request(
        SWF.poll_for_decision_task,
        domain=domain,
        taskList=task_list,
        **kwargs)

    if result.success:
        return result.result

    return None


def respond_decision_task_completed(token, decisions, execution_context=None):
    """Used by deciders to tell the service that the DecisionTask identified by
    the task_token has successfully completed. The decisions argument specifies
    the list of decisions made while processing the task.

    A DecisionTaskCompleted event is added to the workflow history. The
    executionContext specified is attached to the event in the workflow
    execution history.

    token (string) -- [REQUIRED]
    The task_token from the DecisionTask .

    decisions (list) --
    The list of decisions (possibly empty) made by the decider while processing
    this decision task. See the docs for the decision structure for details.

    execution_context (string) --
    User defined context to add to workflow execution.

    returns Boolean
    """
    kwargs = {}

    if execution_context:
        kwargs['executionContext'] = execution_context

    result = make_request(
        SWF.respond_decision_task_completed,
        taskToken=token,
        decisions=decisions,
        **kwargs)

    if result.success:
        return result.result

    return None


def get_decision_manager():
    return Layer1Decisions()
