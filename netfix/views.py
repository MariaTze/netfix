# netfix/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from users.forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from users.models import User, Customer, Company
from services.models import Service, ServiceRequest

def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def customer_profile(request, name):
    user = get_object_or_404(User, username=name, is_customer=True)
    customer = get_object_or_404(Customer, user=user)
    service_requests = (
        ServiceRequest.objects
        .filter(customer=customer)
        .order_by('-requested_at')
    )
    return render(request, 'users/profile.html', {
        'customer': customer,
        'service_requests': service_requests,
    })


@login_required
def company_profile(request, username):
    user = get_object_or_404(User, username=username, is_company=True)
    company = get_object_or_404(Company, user=user)
    services = (
        Service.objects
        .filter(company=company)
        .order_by('-created_at')
    )
    return render(request, 'users/profile.html', {
        'company': company,
        'services': services,
    })

def page_not_found(request, exception):
    # DEBUG LINE
    # print(">>> Custom 404 view triggered")

    return render(request, "errors/404.html", status=404)