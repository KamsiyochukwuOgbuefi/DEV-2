from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, CompanyOverview
from service.models import Service, ServiceProcess
from staff.models import Staff
from django.contrib.auth.decorators import login_required
from accounts.views import login
from accounts.models import Account
from .forms import CompanyForm, CompanyOverviewForm
from django.contrib import messages
from staff.models import Staff
from project.models import Project, ProjectImages, Partner, Testimonial

def company(request):
    title = "About Us"
    company = Company.objects.select_related('companyoverview').first()
    if not company:
        return render(request, 'company/about_us.html', {'title': title})  # Handle missing company gracefully

    company_overview = company.companyoverview
    services = Service.objects.filter(company=company).select_related('company')
    staffs = Staff.objects.filter(company=company).select_related('company')[:4]
    testimonials = Testimonial.objects.filter(company=company).select_related('company')

    context = {
        'company': company,
        'company_overview': company_overview,
        'services': services,
        'staffs': staffs,
        'title': title,
        'testimonials': testimonials,
    }
    return render(request, 'company/about_us.html', context)

@login_required(login_url='admin_login')
def company_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Company Dashboard"
    company = Company.objects.filter(id=1).select_related('companyoverview').first()
    if not company:
        messages.error(request, 'Company not found.')
        return redirect('login')

    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Company details updated successfully.')
        return redirect('company_dashboard')

    context = {
        'title': title,
        'form': form,
        'company': company,
    }

    return render(request, 'company/company_dashboard.html', context)

@login_required(login_url='admin_login')
def business_overview(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Business Overview"
    company = Company.objects.filter(id=1).select_related('companyoverview').first()
    if not company:
        messages.error(request, 'Company not found.')
        return redirect('login')

    business_overview = company.companyoverview
    form = CompanyOverviewForm(request.POST or None, request.FILES or None, instance=business_overview)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Business Overview details updated successfully.')
        return redirect('business_overview')

    context = {
        'title': title,
        'form': form,
        'business_overview': business_overview,
    }

    return render(request, 'company/business_overview.html', context)
