from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.service_list, name='service_list'),
    path('create/', v.create, name='create_service'),
    path('most-requested/', v.most_requested_services, name='most_requested_services'),
    path('delete/<int:service_id>/', v.delete_service, name='delete_service'),
    path('rate/<int:request_id>/', v.rate_service, name='rate_service'),
    path('cancel-request/<int:req_id>/', v.cancel_service_request, name='cancel_service_request'),
    path('<int:id>/request_service/', v.request_service, name='request_service'),
    path('<int:id>', v.index, name='index'),
    path('<slug:field>/', v.service_field, name='services_field'),

]
