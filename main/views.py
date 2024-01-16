from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import FormModelForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def form_submission(request):
    if request.method == 'POST':
        form = FormModelForm(request.POST)
        if form.is_valid():
            form_instance = form.save()

            email_content = f'From: {form_instance.email}\n' \
                            f'Name: {form_instance.first_name}\n' \
                            f'Message: {form_instance.message}'

            send_mail(
                subject='New Form Submission',
                message=email_content,
                from_email='your-email@example.com',  # Use your domain's email address
                recipient_list=['HanKaiwps@gmail.com'],
                fail_silently=False,
                reply_to=[form_instance.email]  # Include the user's email in 'reply-to'
            )

            return JsonResponse({'status': 'success'})
        else:
            # Return form errors if the form is not valid
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=400)
