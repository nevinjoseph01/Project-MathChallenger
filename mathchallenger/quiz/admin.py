# quiz/admin.py

from django.contrib import admin
from .models import QuesModel,Profile,Leaderboard, Statistic


admin.site.register(QuesModel)
admin.site.register(Profile)
admin.site.register(Leaderboard)
admin.site.register(Statistic)

