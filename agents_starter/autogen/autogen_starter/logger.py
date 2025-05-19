import logging

from autogen_agentchat import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME


def setup_logging():
    logging.basicConfig(level=logging.WARNING)

    # For trace logging.
    trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
    trace_logger.addHandler(logging.StreamHandler())
    trace_logger.setLevel(logging.DEBUG)

    # For structured message logging, such as low-level messages between agents.
    event_logger = logging.getLogger(EVENT_LOGGER_NAME)
    event_logger.addHandler(logging.StreamHandler())
    event_logger.setLevel(logging.DEBUG)
