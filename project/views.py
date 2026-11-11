from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectImages, Partner, Testimonial
from service.models import Service
from company.models import Company
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .forms import ProjectForm, ProjectImageForm, PartnerForm, TestimonialForm
from django.contrib import messages

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    title = "Project: {}".format(project.title)
    project_images = ProjectImages.objects.filter(project=project)[:3]
    context = {
        'project': project,
        'project_images': project_images,
        'title': title,
    }
    return render(request, 'project/project.html', context)

def service_projects(request, service_slug):
    company = Company.objects.all()[0]
    service = Service.objects.get(company=company, slug=service_slug)
    title = "{} Projects".format(service.name)
    projects = Project.objects.filter(service=service)

    display_images = {}
    for project in projects:
        for img in ProjectImages.objects.filter(project=project):
            if project.id == img.project_id:
                if project.id not in display_images:
                    display_images[project.id] = img.image.url

    context = {
        'company': company,
        'services': service,
        'projects': projects,
        'display_images': display_images,
        'title': title,
    }
    return render(request, 'project/service_projects.html', context)

@login_required(login_url = 'admin_login')
def project_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Project Dashboard"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)
    projects = Project.objects.filter(service__in=services)

    if request.method == 'POST':
        form = ProjectForm(company, request.POST)
        if form.is_valid():
            data = Project()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.title = form.cleaned_data['title']
            data.project_scope = form.cleaned_data['project_scope']
            data.project_url = form.cleaned_data['project_url']
            data.completion_date = form.cleaned_data['completion_date']
            data.save()
            messages.success(request, 'Thank you! Your Project has been created.')
            return redirect('project_dashboard')
    else:
        form = ProjectForm(company)

    context = {
        'title': title,
        'form': form,
        'projects': projects,
    }

    return render(request, 'project/project_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_project(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update Project"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)
    projects = Project.objects.filter(service__in=services)

    updated_project = get_object_or_404(Project, id=id)
    form = ProjectForm(company, request.POST or None, instance=updated_project)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('project_dashboard')

    context = {
        'title': title,
        'form': form,
        'projects': projects,
        'updated_project': updated_project,
    }

    return render(request, 'project/project_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_project(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_project = Project.objects.get(id=id)
    deleted_project.delete()
    return redirect('project_dashboard')

@login_required(login_url = 'admin_login')
def project_image_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Project: {}".format(ProjectImages.name)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)
    projects = Project.objects.filter(service__in=services)
    project_images = ProjectImages.objects.filter(project__in=projects)

    if request.method == 'POST':
        form = ProjectImageForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = ProjectImages()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.project = form.cleaned_data['project']
            data.image = form.cleaned_data['image']
            data.name = form.cleaned_data['name']
            data.description = form.cleaned_data['description']
            data.save()
            messages.success(request, 'Thank you! Your Project image has been created.')
            return redirect('project_image_dashboard')
    else:
        form = ProjectImageForm(company)

    context = {
        'title': title,
        'form': form,
        'project_images': project_images,
    }

    return render(request, 'project/project_image_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_project_image(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
     
    title = "Update Project: {}".format(ProjectImages.name)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)
    projects = Project.objects.filter(service__in=services)
    project_images = ProjectImages.objects.filter(project__in=projects)

    updated_project_image = get_object_or_404(ProjectImages, id=id)
    form = ProjectImageForm(company, request.POST or None, request.FILES or None, instance=updated_project_image)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('project_image_dashboard')

    context = {
        'title': title,
        'form': form,
        'project_images': project_images,
        'updated_project_image': updated_project_image,
    }

    return render(request, 'project/project_image_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_project_image(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_project_image = ProjectImages.objects.get(id=id)
    deleted_project_image.delete()
    return redirect('project_image_dashboard')

@login_required(login_url='admin_login')
def partner_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')
    
    title = "Partner Dashboard"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    partners = Partner.objects.filter(company=company)

    if request.method == 'POST':
        form = PartnerForm(company, request.POST, request.FILES)
        if form.is_valid():
            # Using form.cleaned_data to create a new Partner instance
            data = Partner()
            data.company = form.cleaned_data['company']
            data.image = form.cleaned_data['image']
            data.name = form.cleaned_data['name']
            data.save()
            messages.success(request, 'New partner has been added successfully.')
            return redirect('partner_dashboard')
    else:
        form = PartnerForm(company)

    context = {
        'title': title,
        'form': form,
        'partners': partners,
    }

    return render(request, 'partner/partner_dashboard.html', context)

@login_required(login_url='admin_login')
def update_partner(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Update Partner"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    partners = Partner.objects.filter(company=company)

    updated_partner = get_object_or_404(Partner, id=id)
    form = PartnerForm(company, request.POST or None, request.FILES or None, instance=updated_partner)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner has been updated successfully.')
            return redirect('partner_dashboard')

    context = {
        'title': title,
        'form': form,
        'partners': partners,
        'updated_partner': updated_partner,
    }

    return render(request, 'partner/partner_dashboard.html', context)

@login_required(login_url='admin_login')
def delete_partner(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    partner = get_object_or_404(Partner, id=id)
    partner.delete()
    messages.success(request, 'Partner has been deleted successfully.')
    return redirect('partner_dashboard')

def testimonial(request):
    title = "Testimonials"
    # Get the first company object
    company = Company.objects.first()  # Use .first() instead of all()[0] for safety
    # Get all Testimonial objects related to the company
    testimonials = Testimonial.objects.filter(company=company)
    context = {
        'title': title,
        'company': company,
        'testimonials': testimonials,  # Use plural to indicate multiple objects
    }
    return render(request, 'testimonial/testimonials.html', context)

@login_required(login_url='admin_login')
def testimonial_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')
    
    title = "Testimonial Dashboard"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    testimonials = Testimonial.objects.filter(company=company)

    if request.method == 'POST':
        form = TestimonialForm(company, request.POST)
        if form.is_valid():
            # Using form.cleaned_data to create a new Testimonial instance
            data = Testimonial()
            data.company = form.cleaned_data['company']
            data.name = form.cleaned_data['name']
            data.content = form.cleaned_data['content']
            data.company_name = form.cleaned_data['company_name']
            data.location = form.cleaned_data['location']
            data.save()
            messages.success(request, 'New testimonial has been added successfully.')
            return redirect('testimonial_dashboard')
    else:
        form = TestimonialForm(company)

    context = {
        'title': title,
        'form': form,
        'testimonials': testimonials,
    }

    return render(request, 'testimonial/testimonial_dashboard.html', context)

@login_required(login_url='admin_login')
def update_testimonial(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    title = "Update Testimonial"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    testimonial = Testimonial.objects.filter(company=company)

    updated_testimonial = get_object_or_404(Testimonial, id=id)
    form = TestimonialForm(company, request.POST or None, instance=updated_testimonial)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial has been updated successfully.')
            return redirect('testimonial_dashboard')

    context = {
        'title': title,
        'form': form,
        'testimonial': testimonial,
        'updated_testimonial': updated_testimonial,
    }

    return render(request, 'testimonial/testimonial_dashboard.html', context)


@login_required(login_url='admin_login')
def delete_testimonial(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    messages.success(request, 'Testimonial has been deleted successfully.')
    return redirect('testimonial_dashboard')