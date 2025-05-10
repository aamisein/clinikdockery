from django.shortcuts import render

# Create your views here.
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
def calculate_factorial_view(request):
    if request.method == 'POST':
        try:
            number = int(request.POST.get('number', 0))
            # اجرای تسک به صورت ناهمگام
            task = calculate_factorial.delay(number)
            return JsonResponse({
                'task_id': task.id,
                'status': 'Task started'
            })
        except ValueError:
            return JsonResponse({
                'error': 'لطفا یک عدد معتبر وارد کنید'
            }, status=400)
    return JsonResponse({
        'error': 'Method not allowed'
    }, status=405)















