"""
Set up a customized logging.
"""

from logging import basicConfig, INFO

def setup_logging():
    """
    Configure logger.
    """

    basicConfig(
        level=INFO,
        format="[%(levelname)s - %(name)s] %(message)s"
    )