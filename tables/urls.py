from django.urls import path
from . import views

urlpatterns = [
    path('all-details/<str:pk>/', views.AllDetails.as_view(), name="all-details"),
    path('aadhar/', views.AadharView.as_view(), name="Aadhar"),
    path('address/<int:pk>/', views.AddressView.as_view(), name="Address"),
    path('qualification/<int:pk>/', views.QualificationView.as_view(), name="Qualification"),
    path('bank/<int:pk>/', views.BankView.as_view(), name="Bank"),
    path('personal-details/<int:pk>/', views.PersonalDetailsView.as_view(), name="Personal-details"),
    path('past-job-experience/<int:pk>/', views.PastJobExperienceView.as_view(), name="Past-job-experience"),
]