from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = "An error occurred"
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                message = str(response.data['detail'])
            else:
                # Format validation errors cleanly
                errors = []
                for field, error_list in response.data.items():
                    if isinstance(error_list, list):
                        errors.append(f"{field}: {', '.join([str(e) for e in error_list])}")
                    else:
                        errors.append(f"{field}: {error_list}")
                message = " | ".join(errors)
        elif isinstance(response.data, list):
            message = " | ".join([str(e) for e in response.data])

        response.data = {
            'success': False,
            'message': message,
            'data': None
        }
    else:
        # Fallback for unhandled server exceptions (500)
        return Response(
            {
                'success': False,
                'message': str(exc) if str(exc) else 'Internal Server Error',
                'data': None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
