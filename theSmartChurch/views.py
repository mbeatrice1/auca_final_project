from django import template
from datetime import date, datetime, timedelta
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import InstanceCheckMeta
from django.db.models.query_utils import refs_expression
# from django.http.response import HttpResponse
from .utils import render_to_pdf
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Appointment, Congregants, Give,JoinService, Profile, Project, Wedding
from .forms import CreateUserForm, NewProjectForm, ProfileUpdateForm, AnnouncementForm, CongForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer, AnnouncementsSerializer
from django.shortcuts import render
import six
import datetime as DT
import dateutil.relativedelta as REL
from django.views.generic.base import TemplateView
from django.db.models import Count
import requests
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import sweetify
from django.db.models import Sum
from .forms import GiveForm
import math, random
from django.views.decorators.http import require_http_methods



def index(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'index.html', {'projects': projects})


def footer(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'footer.html', {'projects': projects})

def nav(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'nav.html', {'projects': projects})



def donateForm(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'donateForm.html', {'projects': projects})


def about(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'about.html', {'projects': projects})


class give(TemplateView):
    template_name = 'give.html'


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['key'] = settings.RAVE_PUBLIC_KEY
    return context


def give(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'give.html', {'projects': projects})


def watch(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'watch.html', {'projects': projects})


def sermons(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'sermons.html', {'projects': projects})


def success(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'success.html', {'projects': projects})


def allUsers(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'allUsers.html', {'projects': projects})

def register(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = User.objects.get(username=username)

            profile = Profile.objects.create(user=user, email=email)
            user = authenticate(username=username, password=password)
            messages.success(request, "Account was created for "+username)
            # login(request, user)
            return redirect('index')
    else:
        form = CreateUserForm()
    return render(request, 'registration/registration_form.html')


@login_required(login_url='/accounts/login/')
def rate_project(request, project_id):
    project = Project.objects.get(id=project_id)
    print(project.title)
    return render(request, "project.html", {"project": project})


@login_required(login_url='/accounts/login/')
def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    projects = Project.objects.filter(user=profile.user).all()
    print(profile.user)
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'projects': projects,
        'profile': profile,
    }
    return render(request, "myProfile.html", context=context)


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    projects = Project.objects.filter(user=profile.user).all()
    print(profile.user)
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'projects': projects,
        'profile': profile,
    }
    return render(request, "profile.html", context=context)


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('dashboard')

    else:
        form = NewProjectForm()
    return render(request, 'newProject.html', {"form": form, "current_user": current_user})


@login_required(login_url='/accounts/login/')
def announcement(request):
    current_user = request.user
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = current_user
            announcement.save()
        return redirect('index')

    else:
        form = AnnouncementForm()
    return render(request, 'announcement.html', {"form": form, "current_user": current_user})


def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search(search_term)
        print(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


class ProfileList(APIView):
    def get(self, request, fromat=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)


class ProjectList(APIView):
    def get(self, request, fromat=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)


def christiansR(request):

    today = DT.date.today()
    rd = REL.relativedelta(days=1, weekday=REL.SU)
    next_sunday_date = today + rd
    if request.method == 'POST':
        firstname = request.POST['first']
        lastname = request.POST['second']
        phoneNmber = request.POST['phonenumber']
        add = request.POST['address']
        email = request.POST['email']
        dateRe = next_sunday_date
        chris = JoinService.objects.all().order_by('dateRe').filter(dateRe=dateRe)
        attendee = len(chris)
        if attendee <= round(15*30/100, 0):

            d = str(next_sunday_date)
            christians = JoinService.objects.create(
                firstname=firstname, lastname=lastname, phoneNmber=phoneNmber, add=add, email=email, dateRe=dateRe)
            christians.save()

            d = str(next_sunday_date)
            obj = {
                'sender': 'CALVARY',
                'phone': phoneNmber,
                'sms': 'Dear '+firstname+', You will attend the service on '+d+' in the first service.'
            }
            r = requests.post('https://send.isangegroup.com/',
                              data=json.dumps(obj))
            print('Successfully')
            return render(request, 'christiansR.html', {'message': 'Successfull Registered'})
        else:
            obj = {
                'sender': 'CALVARY',
                'phone': phoneNmber,
                'sms': 'Dear '+firstname+', This Sunday service is full no more space left . Please try next week'
            }
            r = requests.post('https://send.isangegroup.com/',
                              data=json.dumps(obj))
            return render(request, 'christiansR.html', {'message': 'This Sunday service is full no more space left. Please try next week'})

    else:
        return render(request, 'christiansR.html', {'dateReg': next_sunday_date})


def bookwedding(request):

    # today = DT.date.today()
    rd = REL.relativedelta(days=1, weekday=REL.SU)
    # next_sunday_date = today + rd
    if request.method == 'POST':
        groomName = request.POST['groom']
        brideName = request.POST['bride']
        date = request.POST['date']
        phone = request.POST['phone']

        real_date = DT.datetime.strptime(date, "%Y-%m-%d").date()

        if real_date < DT.date.today():
            return render(request, 'book_wedding.html', {'message': 'You can not use the past date'})
        else:
            try:   
                Wedding.objects.get(date=date)
  
                obj = {
                    'sender': 'CALVARY',
                    'phone': phone,
                    'sms': 'Dear '+groomName+', Date Already Booked  . Please try a different date'
                }
                r = requests.post('https://send.isangegroup.com/',
                                data=json.dumps(obj))

                return render(request, 'book_wedding.html', {'message': 'Date Already booked'})
            except ObjectDoesNotExist:
                if groomName is not None:
                    new_date=DT.datetime.strptime(date, '%Y-%m-%d')
                    wedd = Wedding.objects.create(
                        groomName=groomName, brideName=brideName, phone=phone, date=new_date)
                    wedd.save()

                    obj = {
                    'sender': 'CALVARY',
                    'phone': phone,
                    'sms': 'Dear '+groomName+', your wedding date booked successfully, come at church to meet the Pastor.'
                    }
                    r = requests.post('https://send.isangegroup.com/',
                                    data=json.dumps(obj))

                    return render(request, 'book_wedding.html', {'message': 'Successfully Booked'})
            # else:

            #     return render(request, 'book_wedding.html', {'message': 'Date already booked with others'})


        

    else:
        return render(request, 'book_wedding.html', {'message': 'Please Kindly fill the form'})


def appo(request):
    return render(request,'makeAppointment.html')

def makeAppointment(request):

    if request.method == 'POST':
        
        appointee = request.POST['appointee']
        reason = request.POST['reason']
        date = request.POST['date']
        phone = request.POST['phone']
        com=request.POST['com']

        real_date = DT.datetime.strptime(date, "%Y-%m-%d").date()

        if real_date < DT.date.today():
            return render(request, 'makeAppointment.html', {'message': 'You cannot book the  past date!!'})
        else:
            appointment = Appointment.objects.create(
                appointee = appointee,
                reason = reason,
                Date = date,
                phoneNumber = phone,
                comment = com
            )
        return render(request, 'makeAppointment.html', {'message': 'Dear '+appointee+' wait for the approval,you will receive a message when your date has been approved.'})


    return render(request, 'makeAppointment.html', {'message': 'Please fill the form'})

    #else:
        #return render(request, 'makeAppointment.html', {'message': 'Please Kindly fill the form'})
    

def dashboard(request):
    user = request.user
    join=JoinService.objects.all()
    member=Congregants.objects.all()
    weddings=Wedding.objects.all()


    paginator = Paginator(member, 5)

    paginatorWed=Paginator(weddings,5)
    

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_wedding = paginatorWed.get_page(page_number)

    total_registered_service=join.count()   
    total_congregants=member.count()

    weddings = Wedding.objects.all()
    totalWeddings= weddings.count()

    pastorAppoints = Appointment.objects.all()
    paginatoraApps = Paginator(pastorAppoints,5)
    page_obj_apps = paginatoraApps.get_page(page_number)

    totalPastorAppoints= pastorAppoints.count()

    donation=Give.objects.all()
    paginatorDonation=Paginator(donation,10)
    page_obj_app = paginatorDonation.get_page(page_number)

    sum_donation=Give.objects.all().aggregate(Sum('amount')).get('amount__sum')

    #date=join.filter()

    context={
        'join':join,
        'page_obj':page_obj,
        'total_registered_service':total_registered_service,
        'total_congregants':total_congregants,  
        'weddings':weddings,
        'totalWeddings':totalWeddings,
        'totalPastorAppoints':totalPastorAppoints,
        'pastorAppoints':pastorAppoints,
        'donation':donation,
        'sum_donation': sum_donation,
        'user': user,
        'paginatorWed':paginatorWed,
        'page_obj_wedding':page_obj_wedding,
        'page_obj_app':page_obj_app,
        'page_obj_apps':page_obj_apps
    }

    return render(request,'dashboard.html',context)

def congre(request):
        
    #today = DT.date.today()
    #rd = REL.relativedelta(days=1, weekday=REL.SU)
    #next_sunday_date = today + rd
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phoneNumber = request.POST['phoneNumber']
        address = request.POST['address']
        DOB=request.POST['DOB']
        email = request.POST['email']
        gender=request.POST['gender']
        maritalStatus=request.POST['maritalStatus']
        date=request.POST['date']
    
        
        congs = Congregants.objects.create(
                firstname=firstname, lastname=lastname, phoneNumber=phoneNumber, address=address, DOB=DOB, email=email,gender=gender,maritalStatus=maritalStatus ,date=date)
        congs.save()

           
        return render(request, 'cong.html', {'message': 'Successfull Registered'})
    else:
            
            return render(request, 'cong.html', {'message': 'Please try again'})

   
def updateCongregant(request,pk):
    cong=Congregants.objects.get(id=pk)
    firstName = cong.firstname
    lastName = cong.lastname
    phone = cong.phoneNumber
    address = cong.address
    dob = cong.DOB
    email = cong.email
    gender = cong.gender
    maritalStatus = cong.maritalStatus
    date = cong.date

    context = {'firstName': firstName, 'lastName': lastName, 'phone': phone, 'address': address, 'dob': dob, 'email': email, 'gender': gender, 'maritalStatus': maritalStatus, 'date': date}
    

    # if request.method=="POST":
    #    new=cong
    # context={
    #         'new':new,
    # }
    return render(request,'cong.html', context)


    

def delete_cong(request,pk):
    member=Congregants.objects.get(id=pk)
    if request.method=="POST":
        member.delete()
        return redirect('dashboard')
    context={
        'member':member
    }
    return render(request,'delete.html',context)

# def give(request):


#     return render(request, )

def createCong(request):

    form = CongForm()
    if(request.method == "POST"):
        form = CongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form':form}
    return render(request, 'cong2.html', context)

def updateCong(request, pk_cong):
    cong = Congregants.objects.get(id=pk_cong)
    form = CongForm(instance=cong)
    if request.method == 'POST':
        form = CongForm(request.POST, instance=cong)
        if form.is_valid:
            form.save()
            # messages.success(request, 'Class has been Updated Successfully')
            return redirect('dashboard')
    context = {'form':form}
    return render(request, 'cong2.html',context)

def approveWedding(request, pk_wedding):
    wedding = Wedding.objects.get(id=pk_wedding)
    wedding.status = 'Approved'

    wedding.save()
    return redirect('dashboard')

def cancelWedding(request, pk_wedding):
    wedding = Wedding.objects.get(id=pk_wedding)
    wedding.status = 'Pending'

    wedding.save()
    return redirect('dashboard')

def approveAppointment(request, pk_appointment):
    appointment = Appointment.objects.get(id=pk_appointment)
    appointment.status = 'Approved'

    appointee = appointment.appointee
    phone = appointment.phoneNumber
    

    obj = {
        'sender': 'CALVARY',
        'phone': phone,
        'sms': 'Dear '+appointee+', cometo meet the pastor on the date you requested , your appointment has been confirmed.'
        }
    r = requests.post('https://send.isangegroup.com/',
                        data=json.dumps(obj))

    appointment.save()

    

    return redirect('dashboard')

def cancelAppointment(request, pk_appointment):
    appointment = Appointment.objects.get(id=pk_appointment)
    appointment.status = 'Pending'

    appointment.save()
    return redirect('dashboard')

def sundayService(request):
    template = get_template('sundayService.html')

    today = DT.date.today()
    rd = REL.relativedelta(days=1, weekday=REL.SU)
    next_sunday_date = today + rd

    sundayMembers = JoinService.objects.filter(dateRe=next_sunday_date)



    context = {'sundayMembers':sundayMembers}
    html = template.render(context)
    pdf= render_to_pdf('sundayService.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def monthlyJoinedMembers(request):
    template = get_template('monthlyJoinedMembers.html')

    last_month = datetime.today() - timedelta(days=30)

    joinedmonthlymembers = Congregants.objects.filter(date__gte=last_month)

    print(joinedmonthlymembers)

    context = {'joinedmonthlymembers':joinedmonthlymembers}
    html = template.render(context)
    pdf= render_to_pdf('monthlyJoinedMembers.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def offeringsReportWeekly(request):
    template = get_template('OfferingsReportWeekly.html')

    last_week = datetime.today() - timedelta(days=7)

    offeringsWeekly = Give.objects.filter(date__gte=last_week)
    sum_donation=Give.objects.filter(date__gte=last_week).aggregate(Sum('amount')).get('amount__sum')


    context = {'offeringsWeekly':offeringsWeekly, 'sum_donation':sum_donation}
    html = template.render(context)
    pdf= render_to_pdf('OfferingsReportWeekly.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Week Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def monthlyJoinedMembers(request):
    template = get_template('monthlyJoinedMembers.html')

    last_month = datetime.today() - timedelta(days=30)

    joinedmonthlymembers = Congregants.objects.filter(date__gte=last_month)

    print(joinedmonthlymembers)

    context = {'joinedmonthlymembers':joinedmonthlymembers}
    html = template.render(context)
    pdf= render_to_pdf('monthlyJoinedMembers.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def offeringsReport(request):
    template = get_template('OfferingsReport.html')

    last_month = datetime.today() - timedelta(days=30)

    offeringsMonthly = Give.objects.filter(date__gte=last_month)
    sum_donation=Give.objects.filter(date__gte=last_month).aggregate(Sum('amount')).get('amount__sum')


    context = {'offerringsMontly':offeringsMonthly, 'sum_donation':sum_donation}
    html = template.render(context)
    pdf= render_to_pdf('OfferingsReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"




def reports(request):
    year =DT.datetime.now().year

    january = Congregants.objects.filter(date__year__gte=year, date__month=1).count()
    february = Congregants.objects.filter(date__year__gte=year, date__month=2).count()
    march = Congregants.objects.filter(date__year__gte=year, date__month=3).count()
    april = Congregants.objects.filter(date__year__gte=year, date__month=4).count()
    may = Congregants.objects.filter(date__year__gte=year, date__month=5).count()
    june = Congregants.objects.filter(date__year__gte=year, date__month=6).count()
    july = Congregants.objects.filter(date__year__gte=year, date__month=7).count()
    august = Congregants.objects.filter(date__year__gte=year, date__month=8).count()
    september = Congregants.objects.filter(date__year__gte=year, date__month=9).count()
    october= Congregants.objects.filter(date__year__gte=year, date__month=10).count()
    november = Congregants.objects.filter(date__year__gte=year, date__month=11).count()
    december = Congregants.objects.filter(date__year__gte=year, date__month=12).count()

    all_W_appointments = Wedding.objects.all().count()
    pending_W_apointments = Wedding.objects.filter(status='Pending').count()
    approved_W_apointments = Wedding.objects.filter(status='Approved').count()


    pending_W_apointments_percent = (pending_W_apointments * 100) / all_W_appointments
    all_W_appointments_percent = (approved_W_apointments * 100) / all_W_appointments

    

    context = {
        
    'january':january, 'february':february, 'march':march, 'april':april, 'may':may,'june':june, 
    'july':july, 'august':august, 'september':september, 'october':october, 'november':november, 'december':december,
    'pending_W_apointments_percent':pending_W_apointments_percent, 'all_W_appointments_percent': all_W_appointments_percent
    }
    return render(request, 'reports.html', context)

def monthlyweAppointment(request):
    template = get_template('appointmentWeReports.html')

    last_month = datetime.today() - timedelta(days=30)

    appointmentWe = Wedding.objects.filter(date__gte=last_month)

    print(appointmentWe)

    context = {'appointmentWe':appointmentWe}
    html = template.render(context)
    pdf= render_to_pdf('appointmentWeReports.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"   

def donate(request):
    if request.method=='POST':
        form = GiveForm(request.POST)
        if form.is_valid():
            name=  form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            amount = form.cleaned_data['amount']

            Give.objects.create(
                name=name,email=email,phone=phone,amount=amount
            )

            return redirect(str(process_payment(name,email,amount,phone)))
    else:
        form = GiveForm()
    context={
        'form':form
    }
    return render(request, 'donateForm.html', context)

def process_payment(name,email,amount,phone):
     auth_token= 'FLWSECK_TEST-bdddad26ca8ee7381c93a167eac0008c-X'
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"RWF",
                "redirect_url":"http://127.0.0.1:8000/callback",
                "payment_options":"mobile_money_rwanda",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Calvary Ministries",
                    "description":"Best store in town",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    return render(request, 'success.html')
        

