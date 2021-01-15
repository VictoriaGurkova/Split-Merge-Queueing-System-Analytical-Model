class Params:

    def __init__(self, lambda1, lambda2, mu,
                 devices_amount, fragments_amounts,
                 queues_capacities):
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.devices_amount = devices_amount  # M
        self.fragments_amounts = fragments_amounts  # [a, b]
        self.queues_capacities = queues_capacities  # [c1, c2]

