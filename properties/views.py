
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Property, PropertyImage, Profile

# =========== HOME WITH SEARCH & FILTER =========
def home(request):
    COUNTIES = [

        ('', 'All Counties'),

        ('Nairobi', 'Nairobi'),

        ('Kiambu', 'Kiambu'),

        ('Nakuru', 'Nakuru'),

        ('Mombasa', 'Mombasa'),

        ('Kisumu', 'Kisumu'),

        ('Uasin Gishu', 'Eldoret'),

        ('Meru', 'Meru'),

        ('Nyeri', 'Nyeri'),

        ('Kakamega', 'Kakamega'),

        ('Bungoma', 'Bungoma'),

        ('Kilifi', 'Kilifi'),

        ('Kwale', 'Kwale'),

        ('Taita Taveta', 'Taita Taveta'),

        ('Machakos', 'Machakos'),

        ('Kitui', 'Kitui'),

        ('Makueni', 'Makueni'),

        ('Garissa', 'Garissa'),

        ('Wajir', 'Wajir'),

        ('Mandera', 'Mandera'),

        ('Marsabit', 'Marsabit'),

        ('Isiolo', 'Isiolo'),

        ('Turkana', 'Turkana'),

        ('West Pokot', 'West Pokot'),

        ('Samburu', 'Samburu'),

        ('Trans Nzoia', 'Trans Nzoia'),

        ('Elgeyo Marakwet', 'Elgeyo Marakwet'),

        ('Nandi', 'Nandi'),

        ('Baringo', 'Baringo'),

        ('Laikipia', 'Laikipia'),

        ('Narok', 'Narok'),

        ('Kajiado', 'Kajiado'),

        ('Kericho', 'Kericho'),

        ('Bomet', 'Bomet'),

        ('Homa Bay', 'Homa Bay'),

        ('Migori', 'Migori'),

        ('Siaya', 'Siaya'),

        ('Vihiga', 'Vihiga'),

        ('Busia', 'Busia'),

        ('Tana River', 'Tana River'),

        ('Lamu', 'Lamu'),

        ('Embu', 'Embu'),

        ('Tharaka Nithi', 'Tharaka Nithi'),

        ('Murang\'a', 'Murang\'a'),

        ('Kirinyaga', 'Kirinyaga'),

        ('Nairobi', 'Nairobi'),  # already there

    ]

    properties = Property.objects.filter(is_available=True).order_by('-created_at')

    search_query = request.GET.get('search', '')
    county = request.GET.get('county', '')
    min_price = request.GET.get('min_price', '')

    if search_query:
        properties = properties.filter(title__icontains=search_query) | \
                     properties.filter(town__icontains=search_query) | \
                     properties.filter(location__icontains=search_query)

    if county:
        properties =properties.filter(county=county)

    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except:
            pass

    context = {
        'properties': properties,
        'search_query': search_query,
        'selected_county': county,
        'counties': COUNTIES,
    }
    return render(request, 'home.html', context)

# Property Detail
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {'property': property})


# Post Property (Protected)
@login_required(login_url='/login/')
def post_property(request):
    if request.method == 'POST':
        try:
            property_obj = Property.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                county=request.POST.get('county'),
                town=request.POST.get('town'),
                location=request.POST.get('location'),
                bedrooms=int(request.POST.get('bedrooms')),
                bathrooms=int(request.POST.get('bathrooms')),
                price=float(request.POST.get('price')),
                landlord=request.user,
                is_available=True,
            )

            images = request.FILES.getlist('images')
            uploaded_count = 0
            for index, image in enumerate(images[:5]):
                if image:
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=image
                    )

                    if index == 0:
                        property_obj.image = image
                        property_obj.save()


                    uploaded_count += 1

            if uploaded_count > 0:
                messages.success(request, f"Your house and photos {uploaded_count} has successfully been added to available houses✅")
            else:
                messages.success(request, "Your house has successfully been added to available houses")

            return redirect('home')

        except Exception as e:
            messages.error(request, f"Sorry we couldn't upload your house at the moment, please try again.:{str(e)}")
            print("Main Error:", e)

    return render(request, 'post_property.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Account created successfully.")
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass
    return render(request, 'login.html')


@login_required()
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def my_properties(request):
    properties = Property.objects.filter(landlord=request.user).order_by('-created_at')
    return render(request, 'my_properties.html', {'properties': properties})

from django.contrib.auth.decorators import login_required

# Edit Property
@login_required(login_url='/login/')
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, landlord=request.user)

    if request.method == 'POST':
        try:
            property_obj.title = request.POST.get('title')
            property_obj.description = request.POST.get('description')
            property_obj.county = request.POST.get('county')
            property_obj.town = request.POST.get('town')
            property_obj.location = request.POST.get('location')
            property_obj.bedrooms = int(request.POST.get('bedrooms'))
            property_obj.bathrooms = int(request.POST.get('bathrooms'))
            property_obj.price = float(request.POST.get('price'))
            property_obj.save()

            # Handle new images (if uploaded)
            images = request.FILES.getlist('images')
            for image in images:
                if image:
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=image
                    )
            messages.success(request, 'House Successfully Updated✅')
            return redirect('my_properties')
        except Exception as e:
            messages.error(request, 'There was a problem while trying to update. Please try again.')
            print("Edit Error:", e)

    return render(request, 'edit_property.html', {'property': property_obj})

#Delete Property
@login_required(login_url='/login/')
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, landlord=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'House successfully deleted✅')
        return redirect('my_properties')

    return render(request, 'delete_property.html', {'property': property_obj})

@login_required(login_url='/login/')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.save()
        messages.success(request, 'Phone number updated✅')
        return redirect('my_properties')
    
    return render(request, 'profile.html', {'profile': profile})