
from urllib.parse import urlparse, urljoin
from flask import request
import logging
import typing
import sys
from werkzeug.local import LocalProxy


def is_safe_url(target) -> bool:
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def getconfig(config, section, key) -> typing.Union[None, str]:
    try:
        v = config.get(section, key)
    except:
        v = None
    return v


def set_attributes(cls, dct : dict):
    for key, value in dct.items():
        setattr(cls, key, value)


