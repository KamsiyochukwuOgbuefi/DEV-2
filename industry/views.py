from django.shortcuts import render, redirect, get_object_or_404
from .models import Industry, IndustryProcess
from company.models import Company
from django.contrib.auth.decorators import login_required
from .forms import IndustryForm, IndustryProcessForm
from django.contrib import messages


def industry(request, slug):
    company = Company.objects.all()[0]
    industry = Industry.objects.select_related('company').get(company=company, slug=slug)
    title = "Industry: {}".format(industry.name)
    industry_processes = IndustryProcess.objects.select_related('company', 'industry').filter(company=company, industry=industry).order_by('id')
    categories = []

    context = {
        'title': title,
        'company': company,
        'industries': industry,
        'industry_processes': industry_processes,
        'categories': categories,
    }
    return render(request, 'industry/industry.html', context)


@login_required(login_url='admin_login')
def industry_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Industry Dashboard"
    company = Company.objects.get(id=1)
    industries = Industry.objects.select_related('company').filter(company=company)

    if request.method == 'POST':
        form = IndustryForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = Industry()
            data.company = form.cleaned_data['company']
            data.name = form.cleaned_data['name']
            data.slug = form.cleaned_data['slug']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Industry has been created.')
            return redirect('industry_dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form for errors.')
    else:
        form = IndustryForm(company)

    context = {
        'title': title,
        'form': form,
        'industries': industries,
    }

    return render(request, 'industry/industry_dashboard.html', context)


@login_required(login_url='admin_login')
def update_industry(request, id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Update Industries"
    company = Company.objects.get(id=1)
    industries = Industry.objects.select_related('company').filter(company=company)

    updated_industry = get_object_or_404(Industry.objects.select_related('company'), id=id)
    form = IndustryForm(company, request.POST or None, request.FILES or None, instance=updated_industry)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Industry updated successfully.')
            return redirect('industry_dashboard')

    context = {
        'title': title,
        'form': form,
        'industries': industries,
        'updated_industry': updated_industry,
    }

    return render(request, 'industry/industry_dashboard.html', context)


@login_required(login_url='admin_login')
def delete_industry(request, id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    deleted_industry = get_object_or_404(Industry, id=id)
    deleted_industry.delete()
    return redirect('industry_dashboard')


@login_required(login_url='admin_login')
def industry_process_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Industry Processes"
    company = Company.objects.get(id=1)
    industries = Industry.objects.select_related('company').filter(company=company)
    industry_processes = IndustryProcess.objects.select_related('company', 'industry').filter(industry__in=industries)

    if request.method == 'POST':
        form = IndustryProcessForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = IndustryProcess()
            data.company = form.cleaned_data['company']
            data.industry = form.cleaned_data['industry']
            data.name = form.cleaned_data['name']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Industry Process has been created.')
            return redirect('industry_process_dashboard')
    else:
        form = IndustryProcessForm(company)

    context = {
        'title': title,
        'form': form,
        'industry_processes': industry_processes,
    }

    return render(request, 'industry/industry_process_dashboard.html', context)

@login_required(login_url='admin_login')
def update_industry_process(request, id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Update Industry Processes"
    company = Company.objects.get(id=1)
    industries = Industry.objects.select_related('company').filter(company=company)
    industry_processes = IndustryProcess.objects.select_related('industry').filter(industry__in=industries)

    updated_ip = get_object_or_404(IndustryProcess.objects.select_related('industry'), id=id)
    form = IndustryProcessForm(company, request.POST or None, request.FILES or None, instance=updated_ip)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Industry Process updated successfully.')
            return redirect('industry_process_dashboard')

    context = {
        'title': title,
        'form': form,
        'industry_processes': industry_processes,
        'updated_ip': updated_ip,
    }

    return render(request, 'industry/industry_process_dashboard.html', context)


@login_required(login_url='admin_login')
def delete_industry_process(request, id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    deleted_industry_processes = get_object_or_404(IndustryProcess, id=id)
    deleted_industry_processes.delete()
    return redirect('industry_process_dashboard')
