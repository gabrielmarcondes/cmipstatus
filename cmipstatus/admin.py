from django.contrib import admin
from cmipstatus.models import Experiment,  Member, People

admin.site.register(Experiment)
admin.site.register(Member)
admin.site.register(People)
