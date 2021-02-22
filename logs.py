import logging

from network_params import Params
from state_pretty import pretty_state

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)


def log_network_configuration(params: Params):
    # TODO: расписать параметры системы
    logger.debug('Network configuration:')
    logger.debug(f'lambda 1 = {params.lambda1}')
    logger.debug(f'lambda 2 = {params.lambda2}')
    logger.debug(f'mu = {params.mu}')
    logger.debug(f'devices amount = {params.servers_number}')
    logger.debug(f'fragments amounts = {params.fragments_numbers}')
    logger.debug(f'queues capacities = {params.queues_capacities}')


def log_message(message):
    logger.debug('\n' + message)


def log_event(event):
    logger.debug('\n<===' + event + '===>')


def log_lost_demand():
    logger.debug('Queue is full - demand is lost')


def log_state(current_state):
    logger.debug('\n' + '=' * 120 + '\n')
    logger.debug('Consider state ' + pretty_state(current_state))


def log_state_config(config):
    logger.debug(f'Queue 1 size = {config["q1"]}')
    logger.debug(f'Queue 2 size = {config["q2"]}')
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
