from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import formmodel

def form_submission(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            formmodel.objects.create(first_name=first_name, last_name=last_name, email=email, message=message)

            send_mail(
                'New Form Submission',
                f'Name: {first_name} {last_name}\nEmail: {email}\nMessage: {message}',
                email,  
                ['HanKaiwps@gmail.com'],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            # Log the error if needed
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)
