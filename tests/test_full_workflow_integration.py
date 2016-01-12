# TEMP HACK TO GET THE PROJECT IN
# import sys
# import os
# sys.path.append(os.getcwd())

import json
import logging
import time
import traceback
import unittest
import uuid

from flow import DomainConfig
from flow import ActivityTypeAlreadyExistsError
from flow import DomainAlreadyExistsError
from flow import WorkflowTypeAlreadyExistsError
from flow import get_workflow_execution_history
from flow import poll_for_activity_task
from flow import poll_for_decision_task
from flow import register_domain
from flow import register_workflow_type
from flow import register_activity_type
from flow import respond_activity_task_completed
from flow import respond_activity_task_failed
from flow import respond_decision_task_completed
from flow import start_workflow_execution
from flow import get_decision_manager


class SimpleWorkflowTest(unittest.TestCase):

    DOMAIN_CONFIG = DomainConfig('flow_test',
                                    'A test workflow domain',
                                    '10'
                                    )

    WORKFLOW_TYPE_NAME = 'TestWorkflow1b'
    WORKFLOW_TYPE_VERSION = '1'
    TASK_LIST = {'name': 'default'}

    ACTIVITY_TYPE_NAME = 'TestActivity1ForWorkflow1g'
    ACTIVITY_TYPE_VERSION = '1'

    def setUp(self):
        try:
            register_domain(self.DOMAIN_CONFIG)
        except DomainAlreadyExistsError:
            pass

        try:
            register_workflow_type(
                self.DOMAIN_CONFIG.domain,
                self.WORKFLOW_TYPE_NAME,
                self.WORKFLOW_TYPE_VERSION,
                description='A test workflow',
                default_task_list=self.TASK_LIST,
                default_task_start_to_close_timeout="20",
                default_execution_start_to_close_timeout="60",
                default_child_policy="REQUEST_CANCEL"
            )
        except WorkflowTypeAlreadyExistsError:
            pass

        try:
            register_activity_type(
                self.DOMAIN_CONFIG.domain,
                self.ACTIVITY_TYPE_NAME,
                self.ACTIVITY_TYPE_VERSION,
                description="A test activity for workflow1",
                default_task_heartbeat_timeout="10",
                default_task_list=self.TASK_LIST,
                default_task_priority=100,
                default_task_start_to_close_timeout="10",
                default_task_schedule_to_start_timeout="10",
                default_task_schedule_to_close_timeout="20"
            )
        except ActivityTypeAlreadyExistsError:
            pass

    def _run_decider(self, domain, task_list, activity_type_name,
                     activity_type_version):
        tries = 0
        decider_task = {}

        # while True:
            # decider_task = poll_for_decision_task(domain, task_list,
                                                # reverse_order=True)

            # if decider_task and decider_task.get('taskToken'):
                # # We've got a decider task and we can move on.
                # break

            # # print 'Decider waiting ...'

            # # time.sleep(2)

            # # tries += 1
            # # # if tries > 10:
            # # if tries > 2:
                # # return
                # # raise Exception("Timeout in decider.")

        # # Events we want to ignore.
        # ignorable = (
            # 'DecisionTaskScheduled',
            # 'DecisionTaskStarted',
            # 'DecisionTaskTimedOut',
        # )

        # # Get the most recent "interesting" event.
        # event = None

        # for task_event in decider_task['events']:
            # if task_event['eventType'] not in ignorable:
                # event = task_event
                # break

        # # We now have a completed event to make a decision on.
        # # We now need to signal the end of our decision process by building a
        # # decision response that we will pass to the
        # # 'respond_decision_task_completed' method.

        # # We have a few different response types to handle.
        # print "Event Type: %s" % (event['eventType'],)

        # decision_manager = get_decision_manager()

        # if event['eventType'] == 'WorkflowExecutionStarted':
            # # Handle the execution being started. This is the time where you'll
            # # trigger the activity tasks. This gives you the power to insert many
            # # async to go fan out. Or just go one by one for serial processing.

            # # Generate an activity id.
            # activity_id = uuid.uuid4().hex

            # _input = event.get('workflowExecutionStartedEventAttributes', {}).get(
                # 'input')

            # # TODO: Add some input once we have a worker.
            # decision_manager.schedule_activity_task(
                # activity_id, activity_type_name, activity_type_version,
                # task_list.get('name'), input=_input)

            # print 'Activity Scheduled ' + activity_id

        # elif event['eventType'] == 'ActivityTaskCompleted':
            # # Handle a successful completion.
            # decision_manager.complete_workflow_execution(
                # result=event['activityTaskCompletedEventAttributes']['result'])

            # print 'Activity successfully completed.'

        # elif event['eventType'] == 'ActivityTaskFailed':
            # # Handle a failed schedule.

            # reason = event['activityTaskFailedEventAttributes']['reason']
            # details = event['activityTaskFailedEventAttributes']['details']

            # print "Activty Task Failure"
            # print "Reason: " + reason
            # print "Details: " + details

            # decision_manager.fail_workflow_execution(reason=reason, details=details)

        # else:
            # # Unhandled, trigger fail mode.
            # decision_manager.fail_workflow_execution(
                # reason='unhandled decision task type; %r' % (event['eventType'],))

        # print "Decision Manager Data %s" % (decision_manager._data,)

        # print "Respond decision complete %s" % (
            # respond_decision_task_completed(decider_task['taskToken'],
                                            # decision_manager._data),)


    def _run_worker(self, domain, task_list, identity=None):
        print 'in worker'

        tries = 0
        activity_task = None

        while True:
            print "Start polling for activity"

            activity_task = poll_for_activity_task(domain, task_list, identity)

            print "Activity Task: %s" % (activity_task,)

            if activity_task and activity_task.get('activityId'):
                break

            print 'Worker waiting ...'

            time.sleep(2)
            tries += 1
            if tries > 10:
                return
                # raise Exception("Timeout in worker.")

        print "\nActivity Task Returned: %s" % (activity_task,)

        reason = None
        details = None

        try:
            result = activity_task.get('input')
        except Exception, e:
            reason = "Error in worker task " + e.message
            details = traceback.format_exc()

        if result:
            result = json.loads(result)

        print "\nAcvity Result Input: %s" % (result,)

        if not reason:
            r = respond_activity_task_completed(
                activity_task['taskToken'],
                json.dumps(result) if result else None
            )
        else:
            r = respond_activity_task_failed(activity_task['taskToken'],
                                            reason, details)

    def test_simple_workflow(self):
        workflow_id = uuid.uuid4().hex

        # TODO: Add some input for our workflow.

        run_id = start_workflow_execution(
            self.DOMAIN_CONFIG.domain,
            workflow_id,
            self.WORKFLOW_TYPE_NAME,
            self.WORKFLOW_TYPE_VERSION,
            _input="[10, 2]"
        )

        logging.info("Run id %s", run_id)

        self.assertIsNotNone(run_id)

        self._print_history(self.DOMAIN_CONFIG.domain, workflow_id, run_id)

        logging.info("Run decider to start.")

        self._run_decider(self.DOMAIN_CONFIG.domain, self.TASK_LIST,
                          self.ACTIVITY_TYPE_NAME, self.ACTIVITY_TYPE_VERSION)

        # print 'Confirm activity task scheduled.'
        # self._print_history(self.DOMAIN_CONFIG.domain, workflow_id, run_id)

        # print 'run test worker 1'

        # self._run_worker(self.DOMAIN_CONFIG.domain, self.TASK_LIST,
                         # 'test worker')

        # print 'run decider 2'

        # self._run_decider(self.DOMAIN_CONFIG.domain, self.TASK_LIST,
                          # self.ACTIVITY_TYPE_NAME, self.ACTIVITY_TYPE_VERSION)

        raise

    def _print_history(self, domain, workflow_id, run_id, wait_time=0):
        if wait_time:
            time.sleep(wait_time)

        history = get_workflow_execution_history(domain, workflow_id, run_id)

        print "History"
        for event in history:
            print 'History Event %s' % (event,)
            print 40 * '-'
        # for event in history.pop('events', []):
            # print 'History Event %s' % (event,)
            # print 40 * '-'
