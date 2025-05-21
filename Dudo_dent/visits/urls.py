from django.urls import path, include
from Dudo_dent.visits import views
urlpatterns = [
    path('', views.all_visits, name='all-visits'),
    path('<int:pk>/', include([
        path('', views.visit_by_id, name='visit-details'),
        path('edit-visit/', views.edit_visit, name='edit-visit'),
        path('delete-visit/', views.delete_visit, name='delete-visit'),

    ])),
    path('add-visit/', views.add_visit, name='add-visit'),
]