from django.urls import path,include

from Dudo_dent.procedures import views
urlpatterns = [
    path('', views.all_procedures, name='all-procedures'),
    path('add-procedure/', views.add_procedure, name='add-procedure'),
    path('<int:pk>/', include([
        path('',views.procedure_details, name='procedure-details'),
        path('edit-procedure/', views.edit_procedure, name='edit-procedure'),
        path('delete-procedure/', views.delete_procedure, name='delete-procedure'),
    ])),
]