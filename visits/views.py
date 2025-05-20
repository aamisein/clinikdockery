from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Visit
from .forms import VisitForm, AppointmentSearchForm
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import jdatetime
from jalali_date import datetime2jalali, date2jalali
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from kavenegar import *
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    form_class = VisitForm
    template_name = 'visit/register_visit.html'
    success_url = reverse_lazy('visits:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['today'] = today
        context['todayVisit'] = Visit.objects.filter(current_visit_date=today)
        context['todayTurns'] = Visit.objects.filter(next_visit_date=today)
        return context
 
class VisitSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'    

class VisitListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'visit/visit_list.html'
    context_object_name = 'visits'
    paginate_by = 12

    def get_queryset(self):
        queryset = Visit.objects.all().order_by('-current_visit_date')
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(service__name__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'visit/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 12

    def get_queryset(self):
        queryset = Visit.objects.filter(next_visit_date__isnull=False).order_by('next_visit_date')
        form = AppointmentSearchForm(self.request.GET)
        
        if form.is_valid() and form.cleaned_data['date']:
            search_date = form.cleaned_data['date']
            queryset = queryset.filter(next_visit_date=search_date)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentSearchForm(self.request.GET)
        return context

class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = 'visit/visit_update.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('visits:visit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ویرایش ویزیت'
        return context

class VisitDeleteView(LoginRequiredMixin, DeleteView):
    model = Visit
    template_name = 'visit/visit_confirm_delete.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('visits:visit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف ویزیت'
        return context

@login_required
def home(request):
    return render(request, 'visits/home.html')

@login_required
def register_visit(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            
            # ارسال پیامک به بیمار
            try:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
                params = {
                    'receptor': visit.phone,
                    'template': 'visit-confirmation',
                    'token': visit.first_name,
                    'token2': visit.service.name,
                    'token3': visit.current_visit_date.strftime('%Y/%m/%d'),
                }
                response = api.verify_lookup(params)
                messages.success(request, 'پیامک تایید با موفقیت ارسال شد.')
                logger.info(f'SMS sent successfully to {visit.phone} for visit on {visit.current_visit_date}')
            except APIException as e:
                error_msg = f'خطا در ارسال پیامک: {str(e)}'
                messages.warning(request, error_msg)
                logger.error(f'SMS API error for {visit.phone}: {str(e)}')
            except HTTPException as e:
                error_msg = f'خطا در ارسال پیامک: {str(e)}'
                messages.warning(request, error_msg)
                logger.error(f'SMS HTTP error for {visit.phone}: {str(e)}')
            except Exception as e:
                error_msg = f'خطای غیرمنتظره در ارسال پیامک: {str(e)}'
                messages.warning(request, error_msg)
                logger.error(f'Unexpected error sending SMS to {visit.phone}: {str(e)}')
            
            messages.success(request, 'ویزیت با موفقیت ثبت شد.')
            return redirect('register_visit')
    else:
        form = VisitForm()
    
    today = timezone.now()
    todayVisit = Visit.objects.filter(current_visit_date__date=today.date())
    todayTurns = Visit.objects.filter(next_visit_date__date=today.date())
    
    return render(request, 'visit/register_visit.html', {
        'form': form,
        'today': today,
        'todayVisit': todayVisit,
        'todayTurns': todayTurns
    })















