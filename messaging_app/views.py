# Import System Modules
import logging

# Import Third-party Python Modules
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

# Import Project Modules
from api.messages import messages
from .models import UserMessage
from .serializers import UserMessageSerializer
from googletrans import Translator

# Logger variables to be used for logging
info_logger = logging.getLogger('api_info_logger')
error_logger = logging.getLogger('api_db_error_logger')

User = get_user_model()


class UserMessageViewSet(viewsets.ModelViewSet):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            sender = request.user
            receiver = User.objects.get(pk=pk)
            content = request.data.get('content')

            # Create message
            message = UserMessage.objects.create(sender=sender, receiver=receiver, content=content)

            # Translate content to receiver's language
            translator = Translator()
            lang = request.headers.get('Accept-Language', 'en')
            print("content", content)
            translated_content = translator.translate(content, dest=lang).text

            response_data["result"] = {'message': translated_content}
            response_data["message"] = messages['common']['api_success']['msg']
            response_data["status_code"] = messages['common']['api_success']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data, status=status.HTTP_201_CREATED)
