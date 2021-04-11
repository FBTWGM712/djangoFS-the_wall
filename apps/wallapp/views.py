from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session.keys():
        return redirect ('/success')
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            print(pw_hash)   

            new_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash)
            print(new_user)
            request.session['user_id'] = new_user.id
            request.session['user_name'] = f"{new_user.name} {new_user.alias}"
            request.session['status'] = "registered"

        return redirect("/success") # nunca renderizar en una publicación, ¡siempre redirigir!
    return redirect("/")

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(alias=request.POST['alias'])
            if user:
                logged_user = user[0] #solo hay un usuario con ese alias, por lo que se usa [0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    request.session['user_name'] = f"{logged_user.name} {logged_user.alias}"
                    request.session['status'] = "Logged in"
            
                    return redirect('/success')
                else: 
                    messages.error(request, "password invalid")
        return redirect("/")

def success(request):
    if 'user_name' not in request.session:
        return redirect('/')
    context = {
        'name': request.session['user_name'],
        'messages': Message.objects.all(),
        'comments': Comment.objects.all(),
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add_message(request):
    if request.method == 'POST':
        new_message = Message.objects.create(
            message=request.POST['add_message'], 
            user = User.objects.get(id = request.session['user_id']) ###?????????
        )
    new_message.save()
    messages.success(request,'Message posted successfully.')

    return redirect('/success')

def comment(request):
    print('*'*100)
    print('posting comment...')
    if request.method == 'POST':
        new_comment = Comment.objects.create(
            comment=request.POST['comment'],
            user=User.objects.get(id=request.session['user_id']),
            message=Message.objects.get(id = request.POST['message_ID']) 
        )
        new_comment.save()
    return redirect('/success') 

def delete_message(request, id):
    m = Message.objects.get(id=id)
    m.delete()
    return redirect('/success') 

