import logging

from flow.api import make_request

from flow.core import SWF

from flow.core import check_and_add_kwargs

from flow.faults import ACITVITY_TYPE_ALREADY_EXISTS
from flow.faults import ActivityTypeAlreadyExistsError
from flow.faults import RegisterActivityError

# TODO: List activity types


def register_activity_type(
    domain, name, version, description=None,
    default_task_start_to_close_timeout=None,
    default_task_heartbeat_timeout=None, default_task_list=None,
    default_task_priority=None, default_task_schedule_to_start_timeout=None,
    default_task_schedule_to_close_timeout=None):
    """Registers a new activity type along with its configuration settings in
    the specified domain.

    WARNING
    A TypeAlreadyExists fault is returned if the type already exists in the
    domain. You cannot change any configuration settings of the type after its
    registration, and it must be registered as a new version.

    http://boto3.readthedocs.org/en/latest/reference/services/swf.html#SWF.Client.register_activity_type

    domain (string) -- [REQUIRED]
    The name of the domain in which this activity is to be registered.

    name (string) -- [REQUIRED]
    The name of the activity type within the domain.

    version (string) -- [REQUIRED]
    The version of the activity type.

    description (string) --
    A textual description of the activity type.

    default_task_start_to_close_timeout (string) --
    If set, specifies the default maximum duration that a worker can take to
    process tasks of this activity type. This default can be overridden when
    scheduling an activity task using the ScheduleActivityTask decision.

    default_task_heartbeat_timeout (string) --
    If set, specifies the default maximum time before which a worker processing
    a task of this type must report progress by calling
    RecordActivityTaskHeartbeat. If the timeout is exceeded, the activity task
    is automatically timed out. This default can be overridden when scheduling
    an activity task using the ScheduleActivityTask decision. If the activity
    worker subsequently attempts to record a heartbeat or returns a result, the
    activity worker receives an UnknownResource fault. In this case, Amazon SWF
    no longer considers the activity task to be valid; the activity worker
    should clean up the activity task.

        The duration is specified in seconds; an integer greater than or equal
        to 0. The value "NONE" can be used to specify unlimited duration.

    default_task_list (dict) --
    If set, specifies the default task list to use for scheduling tasks of this
    activity type. This default task list is used if a task list is not provided
    when a task is scheduled through the ScheduleActivityTask decision.

        name (string) -- [REQUIRED]
        The name of the task list.

    default_task_priority (int) --
    The default task priority to assign to the activity type. If not assigned,
    then "0" will be used. Valid values are integers that range from Java's
    Integer.MIN_VALUE (-2147483648) to Integer.MAX_VALUE (2147483647). Higher
    numbers indicate higher priority.

    default_task_schedule_to_start_timeout (string) --
    If set, specifies the default maximum duration that a task of this activity
    type can wait before being assigned to a worker. This default can be
    overridden when scheduling an activity task using the ScheduleActivityTask
    decision.

    default_task_schedule_to_close_timeout (string) --
    If set, specifies the default maximum duration for a task of this activity
    type. This default can be overridden when scheduling an activity task using
    the ScheduleActivityTask decision.

    return None
    """
    kwargs = {}

    for aws_prop, value, conversion in (
        ('description', description, None),
        ('defaultTaskStartToCloseTimeout', default_task_start_to_close_timeout,
         None),
        ('defaultTaskHeartbeatTimeout', default_task_heartbeat_timeout, None),
        ('defaultTaskList', default_task_list, None),
        ('defaultTaskPriority', default_task_priority, str),
        ('defaultTaskScheduleToStartTimeout',
         default_task_schedule_to_start_timeout, None),
        ('defaultTaskScheduleToCloseTimeout',
         default_task_schedule_to_close_timeout, None)):

        kwargs = check_and_add_kwargs(aws_prop, value, conversion, kwargs)

    result = make_request(
        SWF.register_activity_type,
        domain=domain,
        name=name,
        version=version,
        **kwargs)

    if result.success:
        return

    if result.result.code == ACITVITY_TYPE_ALREADY_EXISTS:
        raise ActivityTypeAlreadyExistsError("Workflow type already exists.")

    raise RegisterActivityError(result.result.message)
