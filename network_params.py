class Params:

    def __init__(self, lambda1=1, lambda2=1, mu=3,
                 devices_amount=4, fragments_amounts=None,
                 queue_capacity=None):
        if fragments_amounts is None:
            fragments_amounts = [2, 3]
        if queue_capacity is None:
            queue_capacity = [5, 5]
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.devices_amount = devices_amount  # M
        self.fragments_amounts = fragments_amounts  # [a, b]
        self.queue_capacity = queue_capacity  # [c1, c2]

