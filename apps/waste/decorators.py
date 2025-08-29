from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='20/m', block=True)
def create_pickup(...):
    ...
