class NotificationsChainManager:
    def __init__(self, handlers):
        self.handlers = handlers

    def handle(self, **kwargs):
        for handler in self.handlers:
            handler.handle(**kwargs)
