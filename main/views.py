from django.core.mail import EmailMessage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FormModelSerializer
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='30/m', block=True)
@api_view(['POST'])
def form_submission(request):
    serializer = FormModelSerializer(data=request.data)
    if serializer.is_valid():
        form_instance = serializer.save()

        email_content = f'From: {form_instance.email}\n' \
                        f'Name: {form_instance.first_name} {form_instance.last_name}\n' \
                        f'Message: {form_instance.message}'

        email = EmailMessage(
            subject='New Form Submission',
            body=email_content,
            from_email='hsq0503@gmail.com',  # Use your domain's email address
            to=['HanKaiwps@gmail.com'],  # List of recipients
            headers={'Reply-To': form_instance.email}  # Include the user's email in 'reply-to'
        )

        email.send(fail_silently=False)

        return Response({'status': 'success'})
    else:
        return Response({'errors': serializer.errors}, status=400)
