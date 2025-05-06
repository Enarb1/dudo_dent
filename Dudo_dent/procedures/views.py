from django.shortcuts import render

from Dudo_dent.procedures.models import Procedure


# Create your views here.


def all_procedures(request):
    procedures = Procedure.objects.all().order_by('name')

    context = {
        'procedures': procedures
    }

    return render(request, 'procedures/procedures-main.html', context)


def procedure_details(request, pk):
    procedure = Procedure.objects.filter(pk=pk).first()
    context = {
        'procedure': procedure
    }

    return render(request, 'procedures/procedure-details.html', context)