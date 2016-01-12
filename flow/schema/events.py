from functools import partial

from flow.schema.build import build_tuple


EXECUTION_SCHEMA = {
    'eventTimestamp': 'date',
    'eventType': 'string',
    'eventId': 'number',
    'workflowExecutionStartedEventAttributes': {
        'input': 'string',
        'executionStartToCloseTimeout': 'string',
        'taskStartToCloseTimeout': 'string',
        'childPolicy': 'string',
        'taskList': {
            'name': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'tagList': [
            'string',
        ],
        'taskPriority': 'string',
        'continuedExecutionRunId': 'string',
        'parentWorkflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'parentInitiatedEventId': 'number',
        'lambdaRole': 'string'
    },
    'workflowExecutionCompletedEventAttributes': {
        'result': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'completeWorkflowExecutionFailedEventAttributes': {
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'workflowExecutionFailedEventAttributes': {
        'reason': 'string',
        'details': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'failWorkflowExecutionFailedEventAttributes': {
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'workflowExecutionTimedOutEventAttributes': {
        'timeoutType': 'START_TO_CLOSE',
        'childPolicy': 'string'
    },
    'workflowExecutionCanceledEventAttributes': {
        'details': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'cancelWorkflowExecutionFailedEventAttributes': {
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'workflowExecutionContinuedAsNewEventAttributes': {
        'input': 'string',
        'decisionTaskCompletedEventId': 'number',
        'newExecutionRunId': 'string',
        'executionStartToCloseTimeout': 'string',
        'taskList': {
            'name': 'string'
        },
        'taskPriority': 'string',
        'taskStartToCloseTimeout': 'string',
        'childPolicy': 'string',
        'tagList': [
            'string',
        ],
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'lambdaRole': 'string'
    },
    'continueAsNewWorkflowExecutionFailedEventAttributes': {
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'workflowExecutionTerminatedEventAttributes': {
        'reason': 'string',
        'details': 'string',
        'childPolicy': 'string',
        'cause': 'string',
    },
    'workflowExecutionCancelRequestedEventAttributes': {
        'externalWorkflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'externalInitiatedEventId': 'number',
        'cause': 'CHILD_POLICY_APPLIED'
    },
    'decisionTaskScheduledEventAttributes': {
        'taskList': {
            'name': 'string'
        },
        'taskPriority': 'string',
        'startToCloseTimeout': 'string'
    },
    'decisionTaskStartedEventAttributes': {
        'identity': 'string',
        'scheduledEventId': 'number'
    },
    'decisionTaskCompletedEventAttributes': {
        'executionContext': 'string',
        'scheduledEventId': 'number',
        'startedEventId': 'number'
    },
    'decisionTaskTimedOutEventAttributes': {
        'timeoutType': 'START_TO_CLOSE',
        'scheduledEventId': 'number',
        'startedEventId': 'number'
    },
    'activityTaskScheduledEventAttributes': {
        'activityType': {
            'name': 'string',
            'version': 'string'
        },
        'activityId': 'string',
        'input': 'string',
        'control': 'string',
        'scheduleToStartTimeout': 'string',
        'scheduleToCloseTimeout': 'string',
        'startToCloseTimeout': 'string',
        'taskList': {
            'name': 'string'
        },
        'taskPriority': 'string',
        'decisionTaskCompletedEventId': 'number',
        'heartbeatTimeout': 'string'
    },
    'activityTaskStartedEventAttributes': {
        'identity': 'string',
        'scheduledEventId': 'number'
    },
    'activityTaskCompletedEventAttributes': {
        'result': 'string',
        'scheduledEventId': 'number',
        'startedEventId': 'number'
    },
    'activityTaskFailedEventAttributes': {
        'reason': 'string',
        'details': 'string',
        'scheduledEventId': 'number',
        'startedEventId': 'number'
    },
    'activityTaskTimedOutEventAttributes': {
        'timeoutType': 'string',
        'scheduledEventId': 'number',
        'startedEventId': 'number',
        'details': 'string'
    },
    'activityTaskCanceledEventAttributes': {
        'details': 'string',
        'scheduledEventId': 'number',
        'startedEventId': 'number',
        'latestCancelRequestedEventId': 'number'
    },
    'activityTaskCancelRequestedEventAttributes': {
        'decisionTaskCompletedEventId': 'number',
        'activityId': 'string'
    },
    'workflowExecutionSignaledEventAttributes': {
        'signalName': 'string',
        'input': 'string',
        'externalWorkflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'externalInitiatedEventId': 'number'
    },
    'markerRecordedEventAttributes': {
        'markerName': 'string',
        'details': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'recordMarkerFailedEventAttributes': {
        'markerName': 'string',
        'cause': 'OPERATION_NOT_PERMITTED',
        'decisionTaskCompletedEventId': 'number'
    },
    'timerStartedEventAttributes': {
        'timerId': 'string',
        'control': 'string',
        'startToFireTimeout': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'timerFiredEventAttributes': {
        'timerId': 'string',
        'startedEventId': 'number'
    },
    'timerCanceledEventAttributes': {
        'timerId': 'string',
        'startedEventId': 'number',
        'decisionTaskCompletedEventId': 'number'
    },
    'startChildWorkflowExecutionInitiatedEventAttributes': {
        'workflowId': 'string',
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'control': 'string',
        'input': 'string',
        'executionStartToCloseTimeout': 'string',
        'taskList': {
            'name': 'string'
        },
        'taskPriority': 'string',
        'decisionTaskCompletedEventId': 'number',
        'childPolicy': 'string',
        'taskStartToCloseTimeout': 'string',
        'tagList': [
            'string',
        ],
        'lambdaRole': 'string'
    },
    'childWorkflowExecutionStartedEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'initiatedEventId': 'number'
    },
    'childWorkflowExecutionCompletedEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'result': 'string',
        'initiatedEventId': 'number',
        'startedEventId': 'number'
    },
    'childWorkflowExecutionFailedEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'reason': 'string',
        'details': 'string',
        'initiatedEventId': 'number',
        'startedEventId': 'number'
    },
    'childWorkflowExecutionTimedOutEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'timeoutType': 'START_TO_CLOSE',
        'initiatedEventId': 'number',
        'startedEventId': 'number'
    },
    'childWorkflowExecutionCanceledEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'details': 'string',
        'initiatedEventId': 'number',
        'startedEventId': 'number'
    },
    'childWorkflowExecutionTerminatedEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'initiatedEventId': 'number',
        'startedEventId': 'number'
    },
    'signalExternalWorkflowExecutionInitiatedEventAttributes': {
        'workflowId': 'string',
        'runId': 'string',
        'signalName': 'string',
        'input': 'string',
        'decisionTaskCompletedEventId': 'number',
        'control': 'string'
    },
    'externalWorkflowExecutionSignaledEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'initiatedEventId': 'number'
    },
    'signalExternalWorkflowExecutionFailedEventAttributes': {
        'workflowId': 'string',
        'runId': 'string',
        'cause': 'string',
        'initiatedEventId': 'number',
        'decisionTaskCompletedEventId': 'number',
        'control': 'string'
    },
    'externalWorkflowExecutionCancelRequestedEventAttributes': {
        'workflowExecution': {
            'workflowId': 'string',
            'runId': 'string'
        },
        'initiatedEventId': 'number'
    },
    'requestCancelExternalWorkflowExecutionInitiatedEventAttributes': {
        'workflowId': 'string',
        'runId': 'string',
        'decisionTaskCompletedEventId': 'number',
        'control': 'string'
    },
    'requestCancelExternalWorkflowExecutionFailedEventAttributes': {
        'workflowId': 'string',
        'runId': 'string',
        'cause': 'string',
        'initiatedEventId': 'number',
        'decisionTaskCompletedEventId': 'number',
        'control': 'string'
    },
    'scheduleActivityTaskFailedEventAttributes': {
        'activityType': {
            'name': 'string',
            'version': 'string'
        },
        'activityId': 'string',
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'requestCancelActivityTaskFailedEventAttributes': {
        'activityId': 'string',
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'startTimerFailedEventAttributes': {
        'timerId': 'string',
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'cancelTimerFailedEventAttributes': {
        'timerId': 'string',
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'startChildWorkflowExecutionFailedEventAttributes': {
        'workflowType': {
            'name': 'string',
            'version': 'string'
        },
        'cause': 'string',
        'workflowId': 'string',
        'initiatedEventId': 'number',
        'decisionTaskCompletedEventId': 'number',
        'control': 'string'
    },
    'lambdaFunctionScheduledEventAttributes': {
        'id': 'string',
        'name': 'string',
        'input': 'string',
        'startToCloseTimeout': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'lambdaFunctionStartedEventAttributes': {
        'scheduledEventId': 'number'
    },
    'lambdaFunctionCompletedEventAttributes': {
        'scheduledEventId': 'number',
        'startedEventId': 'number',
        'result': 'string'
    },
    'lambdaFunctionFailedEventAttributes': {
        'scheduledEventId': 'number',
        'startedEventId': 'number',
        'reason': 'string',
        'details': 'string'
    },
    'lambdaFunctionTimedOutEventAttributes': {
        'scheduledEventId': 'number',
        'startedEventId': 'number',
        'timeoutType': 'START_TO_CLOSE'
    },
    'scheduleLambdaFunctionFailedEventAttributes': {
        'id': 'string',
        'name': 'string',
        'cause': 'string',
        'decisionTaskCompletedEventId': 'number'
    },
    'startLambdaFunctionFailedEventAttributes': {
        'scheduledEventId': 'number',
        'cause': 'ASSUME_ROLE_FAILED',
        'message': 'string'
    }
}

create_event_from_map = partial(build_tuple, "Event", EXECUTION_SCHEMA)
