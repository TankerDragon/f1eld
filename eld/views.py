from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Driver, Vehicle, Log
from django.contrib.auth.models import User
from .forms import CreateUserForm, DriverDetailForm, VehicleForm
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LogSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def test(request):
    return render(request, 'test.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('units')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('units')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def units(request):
    return render(request, 'units.html')


@login_required(login_url='login')
def logs(request):
    # User.objects.filter(is_staff = 0).values('id', 'last_login', 'username', 'first_name', 'last_name')
    queryset = Driver.objects.values(
        'id', 'vehicle_id', 'co_driver_id', 'user_id')
    return render(request, 'logs.html', {'drivers': list(queryset)})


@login_required(login_url='login')
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def log(request, id):
    if request.method == 'GET':
        queryset = Log.objects.filter(
            driver_id_id=id).order_by('-date', 'time')
        # return render(request, 'log-week.html', {'logs': list(queryset)})
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response('ok')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        log_id = request.data['id']
        query = Log.objects.filter(driver_id_id=id).get(pk=log_id)
        serializer = LogSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('updated')
    elif request.method == 'DELETE':
        # queryset = Logs.objects.filter(pk = id)
        log_id = request.data['id']
        query = Log.objects.filter(driver_id_id=id).get(pk=log_id)
        query.delete()
        # queryset.delete()
        return Response("deleted")


@login_required(login_url='login')
@api_view(['GET'])
def errors(request, id):
    return render(request, 'errors.html', {'deriver_id': id})


@login_required(login_url='login')
def drivers(request):
    queryset = Driver.objects.select_related('user').all()
    # queryset = User.objects.filter(is_staff=0).values(
    #     'id', 'last_login', 'date_joined', 'username', 'first_name', 'last_name')
    # queryset2 = Drivers.objects.values('co_driver_id', 'vehicle_id','notes','app_version','is_active')
    # print("******")
    # print(Driver.objects.first())
    print(list(queryset))
    return render(request, 'drivers.html', {'drivers': list(queryset)})


@login_required(login_url='login')
def vehicles(request):
    # values('unit_number', 'model', 'vin_number', 'is_active')
    queryset = Vehicle.objects.all()
    return render(request, 'vehicles.html', {'vehicles': list(queryset)})


@login_required(login_url='login')
def new_driver(request):
    user_form = CreateUserForm()

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            # user_form.save()
            print("******")
            print(type(user_form['username']))
            # Drivers.objects.create()
            return redirect('drivers')
    context = {'form': user_form}
    return render(request, 'new-driver.html', context)


@ login_required(login_url='login')
def new_vehicle(request):
    vehicle_form = VehicleForm()

    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        if vehicle_form.is_valid():
            vehicle_form.save()

            # Drivers.objects.create()
            return redirect('vehicles')
    context = {'form': vehicle_form}
    return render(request, 'new-vehicle.html', context)

#!!!!!!!!!!!!!


@ login_required(login_url='login')
def edit_vehicle(request, id):
    vehicle = Vehicle.objects.get(unit_number=id)
    vehicle_form = VehicleForm(instance=vehicle)

    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST, instance=vehicle)
        if vehicle_form.is_valid():
            vehicle_form.save()
            return redirect('vehicles')

    return render(request, 'edit-vehicle.html', {'form': vehicle_form})


@ login_required(login_url='login')
def edit_driver(request, id):
    if not Driver.objects.filter(user_id=id).exists():
        Driver.objects.create(user_id=id)

    user = User.objects.get(id=id)
    user_form = CreateUserForm(instance=user)

    detail = Driver.objects.get(user_id=id)
    detail_form = DriverDetailForm(instance=detail)

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, instance=user)
        detail_form = DriverDetailForm(request.POST, instance=detail)

        if user_form.is_valid() and detail_form.is_valid():
            user.save()
            detail.save()
            return redirect('drivers')
    context = {
        'user_form': user_form,
        'detail_form': detail_form
    }
    return render(request, 'edit-driver.html', context)


# @ login_required(login_url='login')
# def edit_detail(request, id):

#     if request.method == 'POST':
#         if detail_form.is_valid():
#             detail.save()
#             return redirect('drivers')

#     return render(request, 'edit-details.html', {'form': detail_form})
