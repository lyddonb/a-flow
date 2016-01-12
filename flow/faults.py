DOMAIN_ALREADY_EXISTS = 'DomainAlreadyExistsFault'
WORKFLOW_TYPE_ALREADY_EXISTS = 'TypeAlreadyExistsFault'
ACITVITY_TYPE_ALREADY_EXISTS = 'TypeAlreadyExistsFault'


class DomainAlreadyExistsError(Exception):
    pass


class RegisterDomainError(Exception):
    pass


class WorkflowTypeAlreadyExistsError(Exception):
    pass


class RegisterWorkflowTypeError(Exception):
    pass


class ActivityTypeAlreadyExistsError(Exception):
    pass


class RegisterActivityError(Exception):
    pass


class StartWorkflowExecutionError(Exception):
    pass
