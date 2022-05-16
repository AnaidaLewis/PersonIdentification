from django.urls import path
from . import views

urlpatterns = [
    path('all-details/<str:pk>/', views.AllDetails.as_view(), name="all-details"),
    path('address/', views.AddressView.as_view(), name="Address"),
    path('qualification/', views.QualificationView.as_view(), name="Qualification"),
    path('bank/', views.BankView.as_view(), name="Bank"),
    path('personal-details/', views.PersonalDetailsView.as_view(), name="Personal-details"),
    path('past-job-experience/', views.PastJobExperienceView.as_view(), name="Past-job-experience"),
]