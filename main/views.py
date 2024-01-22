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

        # Compose the email content
        email_content = f'Name: {form_instance.first_name} {form_instance.last_name}\n' \
                        f'Email: {form_instance.email}\n' \
                        f'Message: {form_instance.message}'

        # Create an email message with the Django EmailMessage class
        email = EmailMessage(
            subject='New Form Submission',
            body=email_content,
            from_email='your-email@example.com',  # Your email (the sender)
            to=['main-email@example.com'],  # The main email address (recipient)
            cc=[form_instance.email],  # CC to the user's email
            headers={'Reply-To': form_instance.email}  # Reply-To set to the user's email
        )

        # Send the email
        email.send(fail_silently=False)

        return Response({'status': 'success'})
    else:
        return Response({'errors': serializer.errors}, status=400)
