from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .serializers import FormModelSerializer
from .tasks import send_email_task
import logging

logger = logging.getLogger(__name__)

@ratelimit(key='ip', rate='30/m', block=True)
@api_view(['POST'])
def form_submission(request):
    logger.info("Received form submission")
    serializer = FormModelSerializer(data=request.data)
    if serializer.is_valid():
        form_instance = serializer.save()

        # Compose the email content
        email_content = f'Name: {form_instance.first_name} {form_instance.last_name}\n' \
                        f'Email: {form_instance.email}\n' \
                        f'Message: {form_instance.message}'

        # Call the Celery task to send the email
        send_email_task.delay(
            subject='New Form Submission',
            body=email_content,
            from_email='megagrb16@gmail.com',
            to=['HanKaiWps@gmail.com'],
            cc=[form_instance.email]
        )
        logger.info("Form submission successful, email task dispatched")
        return Response({'status': 'success'})
    else:
        logger.error(f"Form submission errors: {serializer.errors}")
        return Response({'errors': serializer.errors}, status=400)
