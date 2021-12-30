from __future__ import absolute_import

import logging

from django.core.mail import mail_admins

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_contact_me_notification(instance):
    '''
    Use SNS to notify Staff of person trying to contact
    us via the Landing Page

    :param instance: ContactMessage object to email
    :return: Nothing
    '''

    message  = '==========================\n'
    message += '%s\n' % instance.name
    message += '%s\n' % instance.email
    message += '==========================\n'
    message += instance.message
    message += '\n'
    message += '==========================\n'

    mail_admins(subject='New Message', message=message)

    return True

