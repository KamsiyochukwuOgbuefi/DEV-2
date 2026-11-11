from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .models import Staff
from django.contrib.auth.decorators import login_required
from .forms import StaffForm
from django.contrib import messages


@login_required(login_url = 'admin_login')
def staff_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Staff Dashboard"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all staff objects associated with the specified company (e.g., Goldridge) from the database
    staffs = Staff.objects.filter(company=company)

    if request.method == 'POST':
        form = StaffForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = Staff()
            data.company = form.cleaned_data['company']
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.position = form.cleaned_data['position']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.is_management = form.cleaned_data['is_management']
            data.is_primary_contact = form.cleaned_data['is_primary_contact']
            data.save()
            messages.success(request, 'Thank you! Your Staff has been created.')
            return redirect('staff_dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    else:
        form = StaffForm(company)

    context = {
        'form': form,
        'staffs': staffs,
        'title': title,
    }

    return render(request, 'team/staff_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_staff(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update Staff"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all staff objects associated with the specified company (e.g., Goldridge) from the database
    staffs = Staff.objects.filter(company=company)

    updated_staff = get_object_or_404(Staff, id=id)
    form = StaffForm(company, request.POST or None, request.FILES or None, instance=updated_staff)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated successfully.')
            return redirect('staff_dashboard')

    context = {
        'form': form,
        'staffs': staffs,
        'title': title,
        'updated_staff': updated_staff,
    }

    return render(request, 'team/staff_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_staff(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_staff = Staff.objects.get(id=id)
    deleted_staff.delete()
    return redirect('staff_dashboard')
