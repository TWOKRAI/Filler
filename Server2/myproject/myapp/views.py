from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Settings

def index(request):
    if request.method == 'POST':
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()

        drink1 = request.POST.get('drink1', 0)
        drink2 = request.POST.get('drink2', 0)
        status = request.POST.get('status', 'false')

        if status == 'true':
            status = True
        else:
            status = False

        print(f"Received data - drink1: {drink1}, drink2: {drink2}, status: {status} {settings.status}")

        if settings.drink1 != drink1:
            print(f"Drink1 changed from {settings.drink1} to {drink1}")
            settings.drink1 = drink1

        if settings.drink2 != drink2:
            print(f"Drink2 changed from {settings.drink2} to {drink2}")
            settings.drink2 = drink2

        if settings.status != status:
            print(f"Status changed from {settings.status} to {status}")
            settings.status = status

        settings.save()

        return JsonResponse({'status': settings.status})

    settings = Settings.objects.first()
    if not settings:
        settings = Settings()
        settings.save()

    return render(request, 'index.html', {'settings': settings})

def settings_view(request):
    if request.method == 'POST':
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()

        todo1 = request.POST.get('todo1', False) == 'on'
        todo2 = request.POST.get('todo2', False) == 'on'

        if settings.todo1 != todo1:
            print(f"Todo1 changed from {settings.todo1} to {todo1}")
            settings.todo1 = todo1

        if settings.todo2 != todo2:
            print(f"Todo2 changed from {settings.todo2} to {todo2}")
            settings.todo2 = todo2

        settings.save()
        return redirect('settings')

    settings = Settings.objects.first()
    if not settings:
        settings = Settings()
        settings.save()

    return render(request, 'settings.html', {'settings': settings})
