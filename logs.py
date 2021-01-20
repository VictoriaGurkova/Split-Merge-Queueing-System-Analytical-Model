import logging

from states_view import pretty_state

logger = logging.getLogger()


def log_message(message):
    logger.debug('===' + message + '===')


def log_state(current_state):
    logger.debug('=' * 150)
    logger.debug('Рассмотрим состояние ' + pretty_state(current_state))


def log_state_config(config):
    logger.debug(f'q1 = {config["q1"]}')
    logger.debug(f'q2 = {config["q2"]}')
    logger.debug(f'devices state = {config["devices"]}')
    logger.debug(f'free devices number = {config["free_devices_number"]}')


def log_arrival_in_queue(lambda_, state, class_id):
    logger.debug(f'Поступление требования {class_id} класса в '
                 f'очередь с интенсивностью {lambda_} и '
                 f'переход в стояние  {pretty_state(state)}')


def log_arrival_on_devices(lambda_, state, class_id):
    logger.debug(f'Поступление требования {class_id} класса с '
                 f'интенсивностью {lambda_} и '
                 f'немедленное начало его'
                 f' обслуживания и переход в состояние {pretty_state(state)}')


def log_leaving_demand(mu, state, class_id):
    logger.debug(f'Завершение обслуживания всего требования '
                 f'{class_id} класса с интенсивностью {mu}, и '
                 f'переход в состояние {pretty_state(state)}')


def log_leaving_fragment(leave_intensity, state, class_id):
    logger.debug(f'Завершение обслуживания фрагмента '
                 f'требования {class_id} класса с '
                 f'интенсивностью {leave_intensity}'
                 f" переход в состояние {pretty_state(state)}")
