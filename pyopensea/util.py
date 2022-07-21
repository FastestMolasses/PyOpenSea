from functools import wraps


def requireApiKey(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.apiKey:
            raise AttributeError('API key is required')
        return func(self, *args, **kwargs)
    return wrapper
