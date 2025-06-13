from django.urls import path, include
from Dudo_dent.visits import views
urlpatterns = [
    path('', views.AllVisits.as_view(), name='all-visits'),
    path('<int:pk>/', include([
        path('', views.VisitDetails.as_view(), name='visit-details'),
        path('edit-visit/', views.edit_visit, name='edit-visit'),
        path('delete-visit/', views.delete_visit, name='delete-visit'),

    ])),
    path('add-visit/', views.VisitCreate.as_view(), name='add-visit'),
]