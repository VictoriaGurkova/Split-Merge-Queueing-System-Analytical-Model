import logging

from states_view import pretty_state

logger = logging.getLogger()


def log_message(message):
    logger.debug('===' + message + '===')


def log_state(current_state):
    logger.debug('=' * 150)
    logger.debug('Consider state ' + pretty_state(current_state))


def log_state_config(config):
    logger.debug(f'q1 = {config["q1"]}')
    logger.debug(f'q2 = {config["q2"]}')
    logger.debug(f'Devices state = {config["devices"]}')
    logger.debug(f'Free devices number = {config["free_devices_number"]}')


def log_arrival_in_queue(lambda_, state, class_id):
    logger.debug(f'Arrival of the {class_id} class demand to '
                 f'the queue with rate {lambda_} and '
                 f'transition to state  {pretty_state(state)}')


def log_arrival_on_devices(lambda_, state, class_id):
    logger.debug(f'Arrival of the {class_id} class demand '
                 f'with rate {lambda_} and '
                 f'immediate start of its service and  '
                 f'transition to state {pretty_state(state)}')


def log_leaving_demand(mu, state, class_id):
    logger.debug(f'Service completion of whole '
                 f'{class_id} class demand with rate {mu} and '
                 f'transition to state {pretty_state(state)}')


def log_leaving_fragment(leave_intensity, state, class_id):
    logger.debug(f'Service completion of '
                 f'{class_id} class demand fragment with '
                 f'rate {leave_intensity} and '
                 f'transition to state {pretty_state(state)}')
