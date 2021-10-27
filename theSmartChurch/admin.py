from django.contrib import admin
from .models import  Appointment, Congregants, Department, JoinService, Parish, Profile,Project, Sermon, Wedding
from .models import Profile,Project
from django.contrib import admin
#from embed_video.admin import AdminVideoMixin
from .models import Item

class MyModelAdmin( admin.ModelAdmin):
    pass
from .models import Profile,Project, Announcements, Give

admin.site.register(Item, MyModelAdmin)
# Register your models here.

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Announcements)
admin.site.register(JoinService)
admin.site.register(Congregants)
admin.site.register(Wedding)
admin.site.register(Appointment)
admin.site.register(Department)
admin.site.register(Sermon)
admin.site.register(Parish)
admin.site.register(Give)




