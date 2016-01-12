from flow.api import make_request

from flow.core import SWF


def poll_for_activity_task(domain, task_list, identity=None):
    """Used by workers to get an ActivityTask from the specified activity
    taskList . This initiates a long poll, where the service holds the HTTP
    connection open and responds as soon as a task becomes available. The
    maximum time the service holds on to the request before responding is 60
    seconds. If no task is available within 60 seconds, the poll will return an
    empty result. An empty result, in this context, means that an ActivityTask
    is returned, but that the value of task_token is an empty string. If a task
    is returned, the worker should use its type to identify and process it
    correctly.

    ** Warning **
        Workers should set their client side socket timeout to at least 70
        seconds (10 seconds higher than the maximum time service may hold the
        poll request).

    domain (string) -- [REQUIRED]
    The name of the domain that contains the task lists being polled.

    task_list (dict) -- [REQUIRED]
    Specifies the task list to poll for activity tasks.
    The specified string must not start or end with whitespace. It must not
    contain a : (colon), / (slash), | (vertical bar), or any control characters
    (u0000-u001f | u007f - u009f). Also, it must not contain the literal string
    quotarnquot.

        name (string) -- [REQUIRED]
        The name of the task list.

    identity (string) --
    Identity of the worker making the request, recorded in the
    ActivityTaskStarted event in the workflow history. This enables diagnostic
    tracing when problems arise. The form of this identity is user defined.

    return dict
    """
    kwargs = {}

    if identity:
        kwargs['identity'] = identity

    result = make_request(
        SWF.poll_for_activity_task,
        domain=domain,
        taskList=task_list,
        **kwargs)

    if result.success:
        return result.result

    return None


def respond_activity_task_completed(task_token, result=None):
    """Used by workers to tell the service that the ActivityTask identified by
    the task_token completed successfully with a result (if provided). The result
    appears in the ActivityTaskCompleted event in the workflow history.

    ** Warning **
        If the requested task does not complete successfully, use
        RespondActivityTaskFailed instead. If the worker finds that the task is
        canceled through the canceled flag returned by
        RecordActivityTaskHeartbeat, it should cancel the task, clean up and
        then call RespondActivityTaskCanceled.

    A task is considered open from the time that it is scheduled until it is
    closed. Therefore a task is reported as open while a worker is processing
    it. A task is closed after it has been specified in a call to
    RespondActivityTaskCompleted, RespondActivityTaskCanceled,
    RespondActivityTaskFailed, or the task has timed out.

    task_token (string) -- [REQUIRED]
    The task_token of the ActivityTask .

    result (string) --
    The result of the activity task. It is a free form string that is
    implementation specific.

    returns success/fail
    """
    kwargs = {}

    if result:
        kwargs['result'] = result

    res = make_request(
        SWF.respond_activity_task_completed,
        taskToken=task_token,
        **kwargs)

    if res.success:
        return res.result

    return None


def respond_activity_task_failed(task_token, reason=None, details=None):
    """Used by workers to tell the service that the ActivityTask identified by
    the task_token has failed with reason (if specified). The reason and details
    appear in the ActivityTaskFailed event added to the workflow history.

    A task is considered open from the time that it is scheduled until it is
    closed. Therefore a task is reported as open while a worker is processing
    it. A task is closed after it has been specified in a call to
    RespondActivityTaskCompleted, RespondActivityTaskCanceled,
    RespondActivityTaskFailed, or the task has timed out .

    task_token (string) -- [REQUIRED]
    The task_token of the ActivityTask .

    reason (string) --
    Description of the error that may assist in diagnostics.

    details (string) --
    Optional. Detailed information about the failure.

    returns None
    """
    kwargs = {}

    if reason:
        kwargs['reason'] = reason

    if details:
        kwargs['details'] = details

    result = make_request(
        SWF.respond_activity_task_failed,
        taskToken=task_token,
        **kwargs)

    if result.success:
        return result.result

    return None



