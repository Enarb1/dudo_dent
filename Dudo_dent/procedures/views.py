from django.shortcuts import render, redirect, get_object_or_404

from Dudo_dent.procedures.models import Procedure
from Dudo_dent.procedures.forms import ProcedureAddForm, ProcedureEditForm, SearchProcedureForm


# Create your views here.


def all_procedures(request):
    procedures = Procedure.objects.all().order_by('name')
    form = SearchProcedureForm(request.GET)

    if request.method == 'GET':
        if form.is_valid():
            query = form.cleaned_data['query']
            procedures = procedures.filter(name__icontains=query).order_by('name')

    context = {
        'procedures': procedures,
        'form': form
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
    return_to = request.GET.get('return_to') or request.POST.get('return_to')

    if request.method == 'POST' and form.is_valid():
        form.save()

        if return_to == 'add-visit':
            return redirect('add-visit')
        return redirect('all-procedures')

    context = {
        'form': form,
        'return_to': return_to
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