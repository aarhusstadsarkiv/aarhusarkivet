import sys
import logging


logger = logging.getLogger(__name__)

if not len(logger.handlers):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)


log = logger

__ALL__ = ['log']
