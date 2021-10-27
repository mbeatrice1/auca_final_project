from django.conf.urls import url,include
from django.conf import settings
from django.db.models.query_utils import PathInfo
from . import views
from django.urls import path

from django.conf.urls.static import static


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^accounts/profile/', views.my_profile, name='my_profile'),
    url(r'register/',views.register, name='register'),
    url(r'project/(\d+)',views.rate_project,name='rate-project'),
    url(r'profile/(\d+)',views.profile,name='profile'),
    url(r'my_profile',views.my_profile,name='my_profile'), 
    url(r'^new/project$', views.new_project, name='new_project'),
    url(r'^annoncement$', views.announcement, name='announcement'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'bookwedding',views.bookwedding,name='bookwedding'), 
    url(r'about',views.about,name='about'), 
    url(r'give',views.give,name='give'), 
    url(r'watch',views.watch,name='watch'), 
    url(r'sermons',views.sermons,name='sermons'), 
    url(r'success', views.success, name='success'), 
    url(r'allUsers', views.allUsers, name='allUsers'), 
    url(r'christiansR',views.christiansR,name='christiansR'),
    url(r'footer', views.footer, name='footer'), 
    url(r'dashboard', views.dashboard, name='dashboard'), 
    url(r'cong', views.congre, name='cong'), 
    path('update/<int:pk_cong>/', views.updateCong,name='update_congregant'),  
    # url(r'donateForm', views.donateForm, name='donateForm'),
    url(r'appointment', views.appo, name='appointment'),
    url(r'makeAppointment', views.makeAppointment, name='makeAppointment'),
    url(r'nav', views.nav, name='nav'),
    #url(r'delete', views.deleteCong, name='delete'),
    path('delete/<int:pk>/',views.delete_cong ,name='Delete_congregant'), 
    path('approve_wedding/<int:pk_wedding>/',views.approveWedding ,name='approve_wedding'), 
    path('cancel_wedding/<int:pk_wedding>/',views.cancelWedding ,name='cancel_wedding'), 
    path('xx/<int:pk_appointment>/',views.approveAppointment ,name='xx'), 
    path('yy/<int:pk_appointment>/',views.cancelAppointment ,name='yy'), 

    url(r'sundayService', views.sundayService, name='sundayService'),
    url(r'monthlyJoinedMembers', views.monthlyJoinedMembers, name='monthlyJoinedMembers'),
     url(r'Zwedding_report', views.monthlyweAppointment , name='appointmentWe'),
    url(r'reports', views.reports, name='reports'),
    url(r'donate', views.donate, name='donate'),
    # path('callback', views.payment_response, name='payment_response'),
    url(r'callback', views.payment_response, name='payment_response'),
    url(r'OfferingsReport', views.offeringsReport, name='OfferingsReport'),
    url(r'OfferingsReportWeekly', views.offeringsReportWeekly, name='OfferingsReportWeekly'),



    
    # path('add_cong',views.createCong ,name='add_cong'), 

    url(r'member_add', views.createCong, name='add_cong'),

    # path('create_update/<int:id>/',views.create_updateCong ,name='add_cong'), 


    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
