from django.shortcuts import render, redirect, HttpResponse
from .models import User
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'logreg_app/index.html')

def success(request):
    return render(request, 'logreg_app/success.html')



def register(request):

    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(key, value, "from views**********")
                messages.error(request, value, key)
                print(f"**********************{messages}" )
                return redirect('/')
        else:
            pwordhash = bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['fn'], last_name=request.POST['ln'], email = request.POST['em'], password = pwordhash)

            request.session['id'] = user.id
            request.session['firstname'] = user.first_name
            request.session['lastname'] = user.last_name
            print(request.session['id'])
            return redirect('/success')

def login(request):
    if request.method == "POST":
        errors = User.objects.validate_login(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
                return redirect('/')
        else:
            user = User.objects.get(email= request.POST['logem'])
            request.session['id'] = user.id
            request.session['firstname'] = user.first_name
            request.session['lastname'] = user.last_name

            return redirect('/success')


def logout(request):
    del request.session['id']
    del request.session['firstname']
    del request.session['lastname']
    return redirect('/')
    