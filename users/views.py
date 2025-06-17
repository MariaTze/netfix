from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Customer, Company
from services.models import Service, ServiceRequest

# TODO: FIX DUPLICATE VIEWS

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
            try:
                tmp = User.objects.get(email=form.cleaned_data['email'])
                user = authenticate(
                    request,
                    username=tmp.username,
                    password=form.cleaned_data['password']
                )
            except User.DoesNotExist:
                user = None
            if user:
                login(request, user)
                return redirect('/')
            # add a form-level error so it renders above the fields
            form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


# CUSTOMER PROFILE
@login_required
def customer_profile(request, username):
    # Fetch the user and customer
    user = get_object_or_404(User, username=username, is_customer=True)
    customer = get_object_or_404(Customer, user=user)
    # Get past service requests, newest first
    service_requests = ServiceRequest.objects.filter(customer=customer).order_by('-requested_at')
    # Determine if we're in edit mode
    edit_mode = request.GET.get('edit') == '1' and request.user == customer.user

    # Handle profile update submission
    if request.method == "POST" and edit_mode:
        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        # Update customer-specific fields
        if 'birth' in request.POST:
            customer.birth = request.POST.get('birth', customer.birth)
        if 'avatar_index' in request.POST:
            customer.avatar_index = request.POST.get('avatar_index', customer.avatar_index)
        customer.save()
        return redirect('users:customer_profile', username=user.username)

    # Render the customer profile template
    return render(request, 'users/customer_profile.html', {
        'customer': customer,
        'service_requests': service_requests,
        'edit_mode': edit_mode,
        'profile_user': customer.user,
    })


# COMPANY PROFILE
@login_required
def company_profile(request, username):
    # Fetch the user and company
    user = get_object_or_404(User, username=username, is_company=True)
    company = get_object_or_404(Company, user=user)
    # Get services for display, newest first
    services = Service.objects.filter(company=company).order_by('-date_created')
    # Determine if we're in edit mode
    edit_mode = request.GET.get('edit') == '1' and request.user == company.user

    # Handle profile update submission
    if request.method == "POST" and edit_mode:
        # Update user fields
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        # Update company-specific fields
        company.avatar_index = request.POST.get('avatar_index', company.avatar_index)
        # If field_of_work is editable, update it
        if 'field_of_work' in request.POST:
            company.field_of_work = request.POST.get('field_of_work', company.field_of_work)
        company.save()
        return redirect('users:company_profile', username=user.username)

    # Render the company profile template
    return render(request, 'users/company_profile.html', {
        'company': company,
        'services': services,
        'edit_mode': edit_mode,
        'profile_user': company.user,
    })
