from django.urls import path
from . import views

urlpatterns = [
    path('api/sessions/<int:pk>', views.Sessions.as_view()),
    path('api/entries/<int:pk>', views.Entries.as_view()),
    path('api/user/<int:pk>', views.Entries.as_view()),
    path('api/users', views.Users.as_view()),
    path('api/entries_month/<int:pk>', views.EntryLastMonth.as_view()),
    path('api/range_date/<int:pk>/<str:date>', views.EntryDateRangeUser.as_view()),
    path('api/date/<int:pk>/<str:date>', views.EntryDateUser.as_view()),
    path('api/range_date_cal/<int:pk>/<str:date>', views.EntryDateRangeUserCalFormat.as_view()),
    path('api/date_details/<int:pk>/<str:date>', views.DayDetailedData.as_view())
]


