from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceProcess
from company.models import Company
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm, ServiceProcessForm
from django.contrib import messages


def service(request, slug):
    company = Company.objects.all()[0]
    service = Service.objects.get(company=company, slug=slug)
    title = "Service: {}".format(service.name)
    service_processes = ServiceProcess.objects.filter(company=company, service=service).order_by('id')
    categories = []

    context = {
        'title': title,
        'company': company,
        'services': service,
        'service_processes': service_processes,
        'categories': categories,
    }
    return render(request, 'service/service.html', context)

@login_required(login_url = 'admin_login')
def service_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Service Dashboard"
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)

    if request.method == 'POST':
        form = ServiceForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = Service()
            data.company = form.cleaned_data['company']
            data.name = form.cleaned_data['name']
            data.slug = form.cleaned_data['slug']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Service has been created.')
            return redirect('service_dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    else:
        form = ServiceForm(company)

    context = {
        'title': title,
        'form': form,
        'services': services,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
     
    title = "Update Services"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)

    updated_service = get_object_or_404(Service, id=id)
    form = ServiceForm(company, request.POST or None, request.FILES or None, instance=updated_service)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Services updated successfully.')
            return redirect('service_dashboard')

    context = {
        'title': title,
        'form': form,
        'services': services,
        'updated_service': updated_service,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_service = Service.objects.get(id=id)
    deleted_service.delete()
    return redirect('service_dashboard')

@login_required(login_url = 'admin_login')
def service_process_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Service Processes"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)
    # Filter service processes based on selected services
    service_processes = ServiceProcess.objects.filter(service__in=services)

    if request.method == 'POST':
        form = ServiceProcessForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = ServiceProcess()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.name = form.cleaned_data['name']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Service Process has been created.')
            return redirect('service_process_dashboard')
    else:
        form = ServiceProcessForm(company)

    context = {
        'title': title,
        'form': form,
        'service_processes': service_processes,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service_process(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update Service Processes"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)
    service_processes = ServiceProcess.objects.filter(service__in=services)

    updated_sp = get_object_or_404(service_processes, id=id)
    form = ServiceProcessForm(company, request.POST or None, request.FILES or None, instance=updated_sp)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Processes updated successfully.')
            return redirect('service_process_dashboard')

    context = {
        'title': title,
        'form': form,
        'service_processes': service_processes,
        'updated_sp': updated_sp,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service_process(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_service_processes = ServiceProcess.objects.get(id=id)
    deleted_service_processes.delete()
    return redirect('service_process_dashboard')
