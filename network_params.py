class Params:

    def __init__(self, lambda1=1, lambda2=1, mu=3,
                 devices_amount=4, fragments_amounts=None,
                 queues_capacities=None):

        if fragments_amounts is None:
            fragments_amounts = [2, 3]
        if queues_capacities is None:
            queues_capacities = [5, 5]

        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.devices_amount = devices_amount  # M
        self.fragments_amounts = fragments_amounts  # [a, b]
        self.queues_capacities = queues_capacities  # [c1, c2]

    def get_lambda(self):
        return self.lambda1 + self.lambda2
