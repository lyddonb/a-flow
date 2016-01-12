import logging

from collections import namedtuple

from boto.swf import exceptions as swf_exceptions

from flow.api import make_request

from flow.core import SWF

from flow.faults import DOMAIN_ALREADY_EXISTS
from flow.faults import DomainAlreadyExistsError
from flow.faults import RegisterDomainError


DomainConfig = namedtuple('DomainConfig', [
    'domain', 'description', 'retention_period'])


# TODO: List domains

def register_domain(domain_config):
    """Registers a new domain.

    Returns None
    """
    try:
        result = make_request(SWF.register_domain,
            name=domain_config.domain,
            description=domain_config.description,
            workflowExecutionRetentionPeriodInDays=domain_config.retention_period)
    except swf_exceptions.SWFDomainAlreadyExistsError:
        logging.debug("Domain already exists.")

    if result.success:
        return

    if result.result.code == DOMAIN_ALREADY_EXISTS:
        raise DomainAlreadyExistsError("Domain already exists.")

    raise RegisterDomainError(result.result.message)
