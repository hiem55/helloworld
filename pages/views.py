# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from .models import Item, ToDoList
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
import pickle
import numpy as np
import logging


def homePageView(request):
    # Retrieve user-submitted values from the request
    sq_ft = request.GET.get('sq_ft')
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    loc = request.GET.get('loc')
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers':[1,2,3,4,5,6,],
        'firstName': 'Justin',
        'lastName': 'Oh'})

def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')

def namePageView(request):
    return render(request, 'justin.html')

def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    print(itemErrandDetail[0].text)
    print(itemErrandDetail[0].todolist_id)
    return render(request, 'ToDoItems.html',
                {'ToDoItemDetail': itemErrandDetail})

from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('message',
                                                kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))
            # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})

def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title })

def logoutView(request):
    logout(request)
    print("*****  You are logged out.")
    return HttpResponseRedirect(reverse('home' ))

def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect('home')
        else:
            # Handle invalid login
            return render(request, 'login.html', {'form': form, 'invalid': True})
    else:
        form = RegisterForm()
        return render(request, 'login.html', {'form': form})

def secretArea(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('message',
               kwargs={'msg': "Please login to access this page.",
                       'title': "Login required."}, ))
    return render(request, 'secret.html', {'useremail': request.user.email })

# Load the trained model from the pickle file
with open('binary_house_price_model.pkl', 'rb') as f:
    model = pickle.load(f)
threshold = 0.5
def predict_house_price(request):
    if request.method == 'POST':
        # Extract form data
        square_feet = int(request.POST.get('sq_ft'))
        bedrooms = int(request.POST.get('bedrooms'))
        bathrooms = int(request.POST.get('bathrooms'))
        location = int(request.POST.get('loc'))

        # Prepare the input data for prediction
        user_input = np.array([[square_feet, bedrooms, bathrooms, location]])

        # Log the form data for debugging
        logging.debug("Form data:")
        logging.debug("Square feet: %s", square_feet)
        logging.debug("Bedrooms: %s", bedrooms)
        logging.debug("Bathrooms: %s", bathrooms)
        logging.debug("Location: %s", location)

        # Make prediction
        predicted_price = model.predict_proba(user_input)[:, 1]  # Get probability of being too expensive

        logging.debug("Predicted price: %s", predicted_price)

        # Classify as expensive or not expensive based on threshold
        if predicted_price[0] > threshold:
            prediction = "Too Expensive"
        else:
            prediction = "Not Expensive"

        logging.debug("Prediction: %s", prediction)

        # Return the predicted price as a response
        return redirect('prediction_result', prediction=prediction)
    # If the request method is not POST, render the form template
    return render(request, 'template.html')

def results(request, sq_ft, bedrooms, bathrooms, loc):

    # Perform any necessary data processing
    with open('binary_house_price_model.pkl', 'rb') as f:
        model = pickle.load(f)
    user_input = np.array([[sq_ft, bedrooms, bathrooms, loc]])
    predicted_price = model.predict(user_input)

    if predicted_price >= 1:
        prediction = "Too Expensive"
    else:
        prediction = "Not Expensive"

    # Render the results page with the extracted data
    return render(request, 'results.html', {
        'sq_ft': sq_ft,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'loc': loc,
        'prediction': prediction
    })

def submit_form(request):
    # Process form submission and extract form data
    sq_ft = int(request.POST.get('sq_ft'))
    bedrooms = int(request.POST.get('bedrooms'))
    bathrooms = int(request.POST.get('bathrooms'))
    loc = int(request.POST.get('loc'))

    # Redirect to the results page with the form data in the query string
    return redirect('results', sq_ft=sq_ft, bedrooms=bedrooms, bathrooms=bathrooms, loc=loc)
