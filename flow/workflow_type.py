import logging

from flow.api import make_request

from flow.core import SWF
from flow.core import check_and_add_kwargs

from flow.faults import WORKFLOW_TYPE_ALREADY_EXISTS
from flow.faults import WorkflowTypeAlreadyExistsError
from flow.faults import RegisterWorkflowTypeError

# TODO: List workflow types


def register_workflow_type(
    domain, name, version, description=None,
    default_task_start_to_close_timeout=None,
    default_execution_start_to_close_timeout=None, default_task_list=None,
    default_task_priority=None, default_child_policy="TERMINATE",
    default_lambda_role=None):
    """Register a workflow type.

    Registers a new workflow type and its configuration settings in the
    specified domain.

    The retention period for the workflow history is set by the RegisterDomain
    action.

    Warning
    If the type already exists, then a TypeAlreadyExists fault is returned. You
    cannot change the configuration settings of a workflow type once it is
    registered and it must be registered as a new version.

    http://boto3.readthedocs.org/en/latest/reference/services/swf.html#SWF.Client.register_workflow_type

    domain (string) -- [REQUIRED]
    The name of the domain in which to register the workflow type.

    name (string) -- [REQUIRED]
    The name of the workflow type.

    version (string) -- [REQUIRED]
    The version of the workflow type.

    description (string) --
    Textual description of the workflow type.

    default_task_start_to_close_timeout (string) --
    If set, specifies the default maximum duration of decision tasks for this
    workflow type. This default can be overridden when starting a workflow
    execution using the StartWorkflowExecution action or the
    StartChildWorkflowExecution decision.

    default_execution_start_to_close_timeout (string) --
    If set, specifies the default maximum duration for executions of this
    workflow type. You can override this default when starting an execution
    through the StartWorkflowExecution action or StartChildWorkflowExecution
    decision.

    default_task_list (dict) --
    If set, specifies the default task list to use for scheduling decision tasks
    for executions of this workflow type. This default is used only if a task
    list is not provided when starting the execution through the
    StartWorkflowExecution action or StartChildWorkflowExecution decision.

        name (string) -- [REQUIRED]
        The name of the task list.

    default_task_priority (int) --
    The default task priority to assign to the workflow type. If not assigned,
    then "0" will be used. Valid values are integers that range from Java's
    Integer.MIN_VALUE (-2147483648) to Integer.MAX_VALUE (2147483647). Higher
    numbers indicate higher priority.

    default_child_policy (string) --
    If set, specifies the default policy to use for the child workflow
    executions when a workflow execution of this type is terminated, by calling
    the TerminateWorkflowExecution action explicitly or due to an expired
    timeout. This default can be overridden when starting a workflow execution
    using the StartWorkflowExecution action or the StartChildWorkflowExecution
    decision.

        The supported child policies are:
        TERMINATE: the child executions will be terminated.
        REQUEST_CANCEL: a request to cancel will be attempted for each child
                        execution by recording a WorkflowExecutionCancelRequested
                        event in its history.  It is up to the decider to take
                        appropriate actions when it receives an execution history
                        with this event.
        ABANDON: no action will be taken. The child executions will continue to run.

    default_lambda_role (string) --
    The ARN of the default IAM role to use when a workflow execution of this
    type invokes AWS Lambda functions.

    return None
    """
    kwargs = {}

    for aws_prop, value, conversion in (
        ('description', description, None),
        ('defaultTaskStartToCloseTimeout', default_task_start_to_close_timeout,
         None),
        ('defaultExecutionStartToCloseTimeout',
         default_execution_start_to_close_timeout, None),
        ('defaultTaskList', default_task_list, None),
        ('defaultTaskPriority', default_task_priority, str),
        ('defaultChildPolicy', default_child_policy, None),
        ('defaultLambdaRole', default_lambda_role, None)):

        kwargs = check_and_add_kwargs(aws_prop, value, conversion, kwargs)

    result = make_request(
        SWF.register_workflow_type,
        domain=domain,
        name=name,
        version=version,
        **kwargs)

    if result.success:
        return

    if result.result.code == WORKFLOW_TYPE_ALREADY_EXISTS:
        raise WorkflowTypeAlreadyExistsError("Workflow type already exists.")

    raise RegisterWorkflowTypeError(result.result.message)
