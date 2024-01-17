from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import FormModelSerializer
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
@api_view(['POST'])
def form_submission(request):
    serializer = FormModelSerializer(data=request.data)
    if serializer.is_valid():
        # Manually validate captcha if required
        # captcha_response = serializer.validated_data['captcha']
        # if not validate_captcha(captcha_response):
        #     return Response({'errors': {'captcha': ['Invalid captcha']}}, status=400)

        form_instance = serializer.save()

        email_content = f'From: {form_instance.email}\n' \
                        f'Name: {form_instance.first_name} {form_instance.last_name}\n' \
                        f'Message: {form_instance.message}'

        send_mail(
            subject='New Form Submission',
            message=email_content,
            from_email='your-email@example.com',  # Use your domain's email address
            recipient_list=['HanKaiwps@gmail.com'],
            fail_silently=False,
            reply_to=[form_instance.email]  # Include the user's email in 'reply-to'
        )

        return Response({'status': 'success'})
    else:
        # Return serializer errors if the data is not valid
        return Response({'errors': serializer.errors}, status=400)
