from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code if renderer_context else 200
        
        # If response is already formatted or an error response handled by exception handler
        if isinstance(data, dict) and ('success' in data or 'detail' in data):
            if 'detail' in data and 'success' not in data:
                data = {
                    'success': False,
                    'message': data['detail'],
                    'data': None
                }
            return super().render(data, accepted_media_type, renderer_context)

        # Standard success envelope
        response_data = {
            'success': status_code < 400,
            'data': data
        }
        return super().render(response_data, accepted_media_type, renderer_context)
