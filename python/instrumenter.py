import wrapt


def wrapper(wrapped, instance, args, kwargs):
    """
    wrap all Lambda invocations and prints a log before calling it.
    """
    request_handler = args[0]
    def _wrapper(event, context):
        print 'This is a log'
        return request_handler(event, context)
    return wrapped(_wrapper, *args[1:], **kwargs)


wrapt.wrap_function_wrapper('__main__', 'handle_event_request', wrapper)
