from django.urls import path,include
from Dudo_dent.procedures import views

urlpatterns = [
    path('', views.AllProcedures.as_view(), name='all-procedures'),
    path('add-procedure/', views.AddProcedure.as_view(), name='add-procedure'),
    path('<int:pk>/', include([
        path('',views.ProcedureDetails.as_view(), name='procedure-details'),
        path('edit-procedure/', views.EditProcedure.as_view(), name='edit-procedure'),
        path('delete-procedure/', views.DeleteProcedure.as_view(), name='delete-procedure'),
    ])),
]