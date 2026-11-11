from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQCategory, FAQQuestion
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .forms import FAQCategoryForm, FAQQuestionForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def faq(request):
    title="Faq Category"
    categories = FAQCategory.objects.all()
    featured = FAQQuestion.objects.select_related('category').order_by('id')[:9]
    context = {
        'title': title,
        'categories': categories,
        'featured': featured,
    }

    return render(request, 'faq/faq.html', context)

def faq_question(request, id=None):
    title="Faq Q&A"
    # Get questions for the selected category
    category = get_object_or_404(FAQCategory, id=id)
    questions = FAQQuestion.objects.filter(category=category)
    categories = FAQCategory.objects.all()
    context = {
        'title': title,
        'category': category,
        'questions': questions,
        'categories': categories,
    }

    return render(request, 'faq/question.html', context)

@login_required(login_url = 'admin_login')
def faqcategory_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title="Category Dashboard"
    faqcategories = FAQCategory.objects.all()
    
    if request.method == 'POST':
        form = FAQCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = FAQCategory()
            data.name = form.cleaned_data['name']
            data.home_note = form.cleaned_data['home_note']
            data.save()
            messages.success(request, 'Thank you! Your FAQ Category has been created.')
            return redirect('faqcategory_dashboard')
    else:
        form = FAQCategoryForm()

    context = {
        'form': form,
        'faqcategories': faqcategories
    }

    return render(request, 'faq/category_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_faqcategory(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_faqcategory = FAQCategory.objects.get(id=id)
    deleted_faqcategory.delete()
    return redirect('faqcategory_dashboard')

@login_required(login_url = 'admin_login')
def update_faqcategory(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update Category Dashboard"
    faqcategories = FAQCategory.objects.all()

    updated_faqcategory = get_object_or_404(FAQCategory, id=id)
    form = FAQCategoryForm(request.POST or None, request.FILES or None, instance=updated_faqcategory)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Dashboard updated successfully.')
            return redirect('faqcategory_dashboard')

    context = {
        'title': title,
        'form': form,
        'faqcategories': faqcategories,
        'updated_faqcategory': updated_faqcategory
    }
    return render(request, 'faq/category_dashboard.html', context)

@login_required(login_url = 'admin_login')
# View for managing FAQ questions in the dashboard
def faqquestion_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title="Faq Q&A Dashboard"
    # Retrieve all FAQ categories from the database
    faqcategories = FAQCategory.objects.all()
    
    # Filter FAQ questions based on selected categories
    faqquestions = FAQQuestion.objects.filter(category__in=faqcategories)
    
    if request.method == 'POST':
        # Process the form data if the request method is POST
        form = FAQQuestionForm(request.POST)
        if form.is_valid():
            # Create a new FAQQuestion instance and save it to the database
            data = FAQQuestion()
            data.category = form.cleaned_data['category']
            data.question = form.cleaned_data['question']
            data.answer = form.cleaned_data['answer']
            data.save()
            messages.success(request, 'Thank you! Your FAQ Q&A has been created.')
            return redirect('faqquestion_dashboard')
    else:
        # If the request method is not POST, create an empty form
        form = FAQQuestionForm()

    # Prepare context to be passed to the template
    context = {
        'title': title,
        'form': form,
        'faqquestions': faqquestions
    }

    # Render the FAQ question dashboard template with the provided context
    return render(request, 'faq/questions_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_faqquestion(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update FAQ Q&A Dashboard"
    faqcategories = FAQCategory.objects.all()
    faqquestions = FAQQuestion.objects.filter(category__in=faqcategories)


    updated_faqquestion = get_object_or_404(faqquestions, id=id)
    form = FAQQuestionForm(request.POST or None, instance=updated_faqquestion)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ Q&A Dashboard updated successfully.')
            return redirect('faqquestion_dashboard')

    context = {
        'title': title,
        'form': form,
        'faqquestions': faqquestions,
        'updated_faqquestion': updated_faqquestion,
    }

    return render(request, 'faq/questions_dashboard.html', context)
    
@login_required(login_url = 'admin_login')
def delete_faqquestion(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_faqquestion = FAQQuestion.objects.get(id=id)
    deleted_faqquestion.delete()
    return redirect('faqquestion_dashboard')
