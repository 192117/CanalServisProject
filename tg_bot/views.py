from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .handler import send_notification


@api_view(['POST'])
def NotificationMessageView(request):
    message = request.data.get('message', '')

    if not message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

    send_notification(message)

    return Response({'success': True}, status=status.HTTP_200_OK)
