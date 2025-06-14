from django.urls import path, include
from Dudo_dent.visits import views

urlpatterns = [
    path('', views.AllVisits.as_view(), name='all-visits'),
    path('add-visit/', views.VisitCreate.as_view(), name='add-visit'),
    path('<int:pk>/', include([
        path('', views.VisitDetails.as_view(), name='visit-details'),
        path('edit-visit/', views.VisitUpdate.as_view(), name='edit-visit'),
        path('delete-visit/', views.DeleteVisit.as_view(), name='delete-visit'),

    ])),
]