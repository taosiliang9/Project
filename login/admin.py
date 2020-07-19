"""
author: taosiliang
create: time: 2020-07-09
update：time: 2020-07-11
"""


# login/admin.py

from django.contrib import admin
from . import models

admin.site.register(models.User)
