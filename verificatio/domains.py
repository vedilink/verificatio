# -*- coding: utf-8 -*-

import requests
import logging
import dns.resolver
from .database import setup_db, retrieve
from .conf import CHECK_TYPES, SERVICE_PREFIX, CNAME_VALUE, FAKE_USER_AGENT
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


# Create db tables if not already created
setup_db()
logger = logging.getLogger(__name__)

class InvalidVerificationType(Exception):
    pass


class NoVerificationCodeExists(Exception):
    pass


def _verify_cname(subdomain, value=CNAME_VALUE):
    try:
        records = dns.resolver.query(subdomain, 'CNAME')
        record = records[0].to_text()
        if record.endswith('.'):
            record = record[:-1]
        if value.endswith('.'):
            value = value[:-1]
        if record == value:
            return True
    except (dns.resolver.NoAnswer, dns.resolver.Timeout):
        logger.debug('', exc_info=True)
    return False


def _verify_txt_record(domain, value):
    """
    Validates a domain by checking that {prefix}={code} is present in the TXT DNS record
    of the domain to check.

    Returns True if verification suceeded.
    """

    token = '{}={}'.format(SERVICE_PREFIX, value)
    try:
        records = dns.resolver.query(domain, 'TXT')
        for r in records:
            record = r.to_text()
            if record.startswith('"') and record.endswith('"'):
                record = record[1:-1]
            if record == token:
                return True
    except (dns.resolver.NoAnswer, dns.resolver.Timeout):
        logger.debug('', exc_info=True)
    return False


class MetaTagParser(HTMLParser):
    """
        Given a meta tag name, saves it's content in value
    """

    def __init__(self, meta_tag_name):
        HTMLParser.__init__(self)
        self.value = None
        self.tag_name = meta_tag_name

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'meta' and attrs.get('name') == self.tag_name:
            self.value = attrs['content']


def _verify_meta_tag(domain, value, tag=SERVICE_PREFIX):
    """
    Validates a domain by checking the existance of a <meta name="{prefix}" content="{code}">
    tag in the <head> of the home page of the domain using either HTTP or HTTPs protocols.

    Returns true if verification suceeded.
    """

    url = '://{}/'.format(domain)
    for proto in ('http', 'https'):
        try:
            r = requests.get(
                proto + url,
                headers={
                    'User-Agent': FAKE_USER_AGENT})
            text = r.text
            parser = MetaTagParser(tag)
            parser.feed(text)
            if bool(parser.value == value):
                return True
        except:
            logger.debug('', exc_info=True)
    return False


def _verify_file_exists(domain, value):
    """
    Validates a domain by checking the existance of a file named {code}.html at the root of the
    website using either HTTP or HTTPS protocols. The file must contain {prefix}={code} in the
    body of the file to ensure the host isn't responding 200 to any requests.

    Returns true if verification suceeded.
    """

    url = '://{}/{}.html'.format(domain, value)
    for proto in ('http', 'https'):
        try:
            r = requests.get(proto + url, headers={'User-Agent': FAKE_USER_AGENT})
            if bool(200 <= r.status_code < 300):
                return True
        except:
            logger.debug('', exc_info=True)
    return False


def verify(domain, check_type):
    """
    Check the ownership of a domain by going through series of strategies.
    If the domain is considered verified, this method returns true.

    The prefix is a fixed DNS safe string like "service-site-verification"
    and the code is a random value associated to this domain. It is advised to
    prefix the code by a fixed value that is unique to the service like
    "service2k3dWdk9dwz".
    """

    code = retrieve(domain, check_type)

    if check_type not in CHECK_TYPES:
        raise InvalidVerificationType(
            '%s not in %s' % (check_type, str(CHECK_TYPES)))

    if code is None:
        raise NoVerificationCodeExists(
            'No verification code found for %s'
            % str((domain, check_type)))

    response = False

    if check_type == 'CNAME':
        response = _verify_cname(code)
    elif check_type == 'TXT':
        response = _verify_txt_record(domain, code)
    elif check_type == 'META':
        response = _verify_meta_tag(domain, code)
    elif check_type == 'FILE':
        response = _verify_file_exists(domain, code)

    return response
