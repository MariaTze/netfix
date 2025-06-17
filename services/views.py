from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from users.models import Company, Customer, User
from .models import Service
from .forms import CreateNewService, RequestServiceForm
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from .forms import RateServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date_created")
    return render(request, 'services/list.html', {'services': services})


def most_requested_services(request):
    services = Service.objects.annotate(
        num_requests=Count('servicerequest')
    ).filter(num_requests__gte=1).order_by('-num_requests', '-date_created')
    return render(request, 'services/most_requested.html', {'services': services})

def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect('home')

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
            messages.success(request, "Service created successfully!")
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

    service = get_object_or_404(Service, id=id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            ServiceRequest.objects.create(
                customer=customer,
                service=service,
                address=form.cleaned_data['address'],
                hours=form.cleaned_data['hours'],
            )
            messages.success(request, "Your service request was submitted successfully!")
            return redirect('services:service_list')
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })
@login_required
def cancel_service_request(request, req_id):
    service_request = get_object_or_404(ServiceRequest, id=req_id, customer=request.user.customer_profile)
    if request.method == "POST":
        service_request.delete()
        messages.success(request, "Your service booking has been cancelled.")
        return redirect('users:customer_profile', username=request.user.username)
    return render(request, 'services/cancel_confirmation.html', {'service_request': service_request})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    # Only allow the company owner to delete
    if hasattr(request.user, 'company_profile') and service.company.user == request.user:
        service.delete()
        messages.success(request, "Service deleted successfully!")
    else:
        messages.error(request, "You are not allowed to delete this service.")
    return redirect('services:service_list')

@login_required
def rate_service(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, customer=request.user.customer_profile)
    if service_request.rating is not None:
        messages.info(request, "You have already rated this service.")
        return redirect('users:customer_profile', username=request.user.username)

    if request.method == "POST":
        form = RateServiceForm(request.POST)
        if form.is_valid():
            service_request.rating = int(form.cleaned_data['rating'])
            service_request.save()
            messages.success(request, "Thank you for rating this service!")
            return redirect('users:customer_profile', username=request.user.username)
    else:
        form = RateServiceForm()

    return render(request, 'services/rate_service.html', {
        'form': form,
        'service_request': service_request,
    })