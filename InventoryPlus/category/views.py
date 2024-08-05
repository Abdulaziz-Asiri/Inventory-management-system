from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from category.models import Category
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="{% url 'account:sign_in'%}")
def all_Categories_view(request: HttpRequest):
    category = Category.objects.all()
    return render(request , "allCategory.html" , {"categories": category})

def add_Category_view(request: HttpRequest):
    if not request.user.is_staff:
        messages.add_message(request, "Sorry, Only Staff who has the access to this page.")
    category = Category.objects.all()
    if request.method == "POST":
        new_Category = Category(name=request.POST['name'], description=request.POST['description'])
        new_Category.save()

     #send confirmation email
        content_html = render_to_string("mail/confirmation.html",{"CategoryName":new_Category}) #set email
        send_to = 'aboodi12356@gmail.com'
        email_message = EmailMessage("confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
        email_message.content_subtype = "html"
        #email_message.connection = email_message.get_connection(True)
        email_message.send()

        messages.success(request, "The category has been add successfully.", "alert-success")
    


    return render(request, "addCategory.html",  {"categories": category})

def delete_Category_view(request:HttpRequest, category_id: int):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect("category:all_Categories_view")


def update_Category_view(request:HttpRequest, category_id: int):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        category.name = request.POST["name"]
        category.description = request.POST["description"]
        category.save()
        return redirect('category:all_Categories_view')
    
    return render("updateCategory.html", {"categories":category})