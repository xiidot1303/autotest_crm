from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from app.forms import *
from django.urls import reverse_lazy
from typing import Dict, Any
from django.contrib import messages
from app.services.string_service import *
from app.utils.deco import *

def redirect_back(request):
    return redirect(request.META.get('HTTP_REFERER'))