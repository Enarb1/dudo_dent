from django.shortcuts import render, redirect, get_object_or_404

from Dudo_dent.procedures.models import Procedure
from Dudo_dent.procedures.forms import ProcedureAddForm, ProcedureEditForm


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


def add_procedure(request):
    form = ProcedureAddForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('all-procedures')

    context = {
        'form': form
    }

    return render(request, 'procedures/add-procedure.html', context)

def edit_procedure(request, pk):
    procedure = get_object_or_404(Procedure, pk=pk)

    if request.method == 'POST':
        form = ProcedureEditForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()
            return redirect('procedure-details', pk=pk)

    else:
        form = ProcedureEditForm(instance=procedure)

    context = {
        'procedure': procedure,
        'form': form
    }

    return render(request, 'procedures/edit-procedure.html', context)


def delete_procedure(request, pk):
    procedure = get_object_or_404(Procedure, pk=pk)

    if request.method == 'POST':
        procedure.delete()
        return redirect('all-procedures')

    return redirect('procedure-details', pk=pk)