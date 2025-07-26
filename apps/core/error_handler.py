from django.http import JsonResponse
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        if response.data.get('detail'):
            response.data['message'] = response.data.get('detail', str(exc))
            del response.data['detail']
    else:
        response = JsonResponse({'message': str(exc), 'status_code': 500})
        response.status_code = 500
    return response
