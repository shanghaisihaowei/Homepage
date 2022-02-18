from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, code=200, message='success', result=[], headers=None, exception=False, **kwargs):
        data = {'code': code, 'message': message, 'result': result}
        if kwargs:
            data.update(kwargs)
        super().__init__(data=data, headers=headers, exception=exception)
