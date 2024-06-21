# Import System Modules
import logging
from datetime import datetime, timedelta

# Import Third-party Python Modules
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Import Project Modules
from api.email import Email
from api.messages import messages
from api.permissions import IsAdmin
from api.serializers import UserLoginSerializer, UserSerializer, ChangePasswordSerializer, UserRegistrationSerializer
from rbac_api.settings import SITE_URL, ENVIRONMENT
from users.models import Profile

# Logger variables to be used for logging

info_logger = logging.getLogger('api_info_logger')
error_logger = logging.getLogger('api_db_error_logger')

User = get_user_model()


class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email/username and password.
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            request_data = request.data
            print("request_data", request_data)
            serializer = UserLoginSerializer(data=request_data)
            if serializer.is_valid():
                user = serializer.validated_data
                serializer = UserSerializer(user)
                token = RefreshToken.for_user(user)
                data = serializer.data
                update_last_login(None, user)

                data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
                response_data["result"] = data
                response_data["message"] = messages['login']['login_success']['msg']
                response_data["status_code"] = messages['login']['login_success']['status_code']
            else:
                print("error", serializer.error_messages)
                response_data["result"] = {}
                response_data["message"] = messages['login']['invalid_credentials']['msg']
                response_data["status_code"] = messages['login']['invalid_credentials']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class RegisterUserView(GenericAPIView):
    """
    An endpoint to create a new User.
    """

    def post(self, request):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}

        try:
            request_data = request.data
            email = request_data.get("email")
            username = request_data.get("username")

            if User.objects.filter(email=email).exists():
                response_data["message"] = messages['registration']['email_exist']['msg']
                response_data["status_code"] = messages['registration']['email_exist']['status_code']
                return Response(response_data)
            if User.objects.filter(username=username).exists():
                response_data["message"] = messages['registration']['username_exist']['msg']
                response_data["status_code"] = messages['registration']['username_exist']['status_code']
                return Response(response_data)

            serializer = UserRegistrationSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                response_data["message"] = messages['registration']['register_success']['msg']
                response_data["status_code"] = messages['registration']['register_success']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class ChangePasswordView(GenericAPIView):
    """
    An endpoint to change User password.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                if not request.user.check_password(serializer.data['old_password']):
                    response_data["message"] = messages['user']['wrong_old_password']['msg']
                    response_data["status_code"] = messages['user']['wrong_old_password']['status_code']
                request.user.set_password(serializer.data['new_password'])
                request.user.save()
                response_data["message"] = messages['user']['password_changed_success']['msg']
                response_data["status_code"] = messages['user']['password_changed_success']['status_code']
                # return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class UserListView(ListAPIView):
    """
    An endpoint to retrieve a list of all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdmin]


class PasswordResetAPIView(GenericAPIView):
    """
    An endpoint to send password reset email.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            request_data = request.data
            email = request_data["email"]

            user = User.objects.filter(email=email, is_active=1).first()
            if user:
                # Generate a password reset token
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = default_token_generator.make_token(user)

                # Construct the reset link
                reset_link = f"{SITE_URL[ENVIRONMENT]}reset-password/{uid}/{token}/"

                # Send email
                from_person = "Admin Team"
                bcc_email = None
                recipient_emails = [user.email]
                username = user.username
                template_file = "email/password_reset.html"

                template_data = {"reset_link": reset_link, "reach_out_person": from_person, "username": username}
                email_subject = 'Password Reset'
                mail = Email()
                mail.send(email_subject, template_file, template_data, recipient_emails, bcc=bcc_email)

                response_data["message"] = messages['user']['password_reset_email_success']['msg']
                response_data["status_code"] = messages['user']['password_reset_email_success']['status_code']
            else:
                response_data["message"] = messages['user']['user_not_found']['msg']
                response_data["status_code"] = messages['user']['user_not_found']['status_code']

        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class PasswordResetConfirmAPIView(GenericAPIView):
    """
    An endpoint to reset the user password.
    """

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            request_data = request.data
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.filter(id=uid, is_active=1).first()
            if user and default_token_generator.check_token(user, token):
                # Proceed with password reset logic here
                new_password = request_data.get('new_password')
                user.set_password(new_password)
                user.save()
                response_data["message"] = messages['user']['password_reset_success']['msg']
                response_data["status_code"] = messages['user']['password_reset_success']['status_code']
            else:
                response_data["message"] = messages['user']['invalid_reset_link']['msg']
                response_data["status_code"] = messages['user']['invalid_reset_link']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class CreateProfileAPIView(GenericAPIView):
    """
    An endpoint to create user profile.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            request_data = request.data
            curr_user = request.user
            bio = request_data.get("bio")

            # Add data into Profile table
            profile_details = {"user": curr_user, "bio": bio}
            Profile.objects.create(**profile_details)
            response_data["message"] = messages['profile']['create_success']['msg']
            response_data["status_code"] = messages['profile']['create_success']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)


class UpdateUserProfileAPIView(GenericAPIView):
    """
    An endpoint to update user profile.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response_data = {"message": messages['common']['api_failed']['msg'],
                         "status_code": messages['common']['api_failed']['status_code'], "result": {}}
        try:
            request_data = request.data
            curr_user = request.user
            bio = request_data.get("bio")

            # Prepare dict for update
            profile_data = {"bio": bio, "modified_on": datetime.now()}
            profile_obj = Profile.objects.filter(user=curr_user).update(**profile_data)
            response_data["message"] = messages['profile']['update_success']['msg']
            response_data["status_code"] = messages['profile']['update_success']['status_code']
        except Exception as e:
            error_logger.error(e, exc_info=True)
        return Response(response_data)
