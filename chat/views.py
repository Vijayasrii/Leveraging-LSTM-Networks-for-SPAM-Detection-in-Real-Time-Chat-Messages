from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from chat.models import Room, Message
from .forms import RegistrationForm
from django.http import JsonResponse, HttpResponse

def index(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    return render(request, 'index.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to login after successful registration
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration.html', {'form': form})



from django.shortcuts import render, redirect
from .forms import RegistrationForm
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            error_message = 'Username or password is incorrect.'
    return render(request, 'login.html', {'error_message': error_message})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

from django.http import HttpResponse
from .models import Message
from model.algorithms.textpreprocessing import clean_text
from model.algorithms.textpreprocessing import predict

from django.http import JsonResponse

from .models import OffensiveMessage

def send(request):
    message = request.POST.get('message')
    username = request.POST.get('username')
    room_id = request.POST.get('room_id')

    # Preprocess the message (assuming this preprocessing is done in preprocess_message function)
    preprocessed_message = clean_text(message)

    # Use the ML model to classify the message
    classification = predict(preprocessed_message)

    # Initialize censored_message
    censored_message = message

    # Censor offensive messages
    if classification == 'offensive':
        censored_message = message[0] + '*'*(len(message)-2) + message[-1]  # Keep first and last characters, replace others with '*'
        # Create an OffensiveMessage object to store the offensive message details
        offensive_msg = OffensiveMessage.objects.create(user=username, room=room_id, message=message)
        # Save the offensive message to the database
        offensive_msg.save()
    # Create a new Message object with the classification result
    new_message = Message.objects.create(value=message, user=username, room=room_id, classification=classification, censored_value=censored_message)
    new_message.save()

    # Include censored_message in the JSON response
    response_data = {
        'original_message': message,
        'censored_message': censored_message,
        'classification': classification
    }

    print(response_data)
    
    return JsonResponse(response_data)


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def logout_view(request):
    if request.method == 'POST':
        # Perform logout logic
        logout(request)
        # Redirect to a specific page after logout (e.g., login page)
        return redirect('login')  # Change 'login' to the desired URL name
    else:
        # Handle GET request (optional)
        return redirect('login') 




def AdminLogin(request):
    if request.method == 'POST':
        usrid = request.POST.get('username')
        pswd = request.POST.get('password')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            print('redirecting to admin base')
            return render(request, 'adminhome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'adminlogin.html')



def AdminHomePage(request):
    return render(request, 'adminhome.html')  

from django.contrib.auth.models import User

def ViewUsersPage(request):
    users = User.objects.all()  # ✅ Correct
    return render(request, 'viewusers.html', {'users': users})
  

def UserActivateFunction(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = True
    user.save()      
    return redirect(ViewUsersPage) 

def UserDeactivateFunction(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = False
    user.save()      
    return redirect(ViewUsersPage)

def UserDeleteFunction(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return redirect('view-users')

# views.py
from django.shortcuts import render

def base(request):
    return render(request, 'base.html')  # or any template you want


def logout_view(request):
    logout(request)
    return redirect('login')
