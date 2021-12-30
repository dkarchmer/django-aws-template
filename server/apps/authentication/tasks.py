import logging
import time

from django.conf import settings
from django.template.defaultfilters import slugify

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_new_user_notification(id, username, email):
    '''
    Information about the ContactMe form is sent via
    SQS to an EB worker, who will then send notifications
    to our Staff

    :param instance: ContactMessage object to email
    :return: Nothing
    '''

    subject = 'User @{0} (ID={1}) has registered with email {2}'.format(username, id, email)

    logger.debug(subject)
