from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from users.models import Company, Customer, User
from .models import Service
from .forms import CreateNewService, RequestServiceForm
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest

def service_list(request):
    services = Service.objects.all().order_by("-date_created")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect('home')  # Or an error page for non-company users

    if request.method == "POST":
        form = CreateNewService(request.POST, company=company)
        if form.is_valid():
            Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                field=form.cleaned_data['field'],
                price_per_hour=form.cleaned_data['price_per_hour'],
                company=company,
            )
            return redirect('services:service_list')
    else:
        form = CreateNewService(company=company)

    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    try:
        customer = request.user.customer_profile
    except Exception:
        return redirect('home')  # Or an error page

    service = Service.objects.get(id=id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            ServiceRequest.objects.create(
                customer=customer,
                service=service,
                address=form.cleaned_data['address'],
                hours=form.cleaned_data['hours'],
            )
            return redirect('services:service_list')
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'form': form, 'service': service})
