from django import forms
from .models import Visit, Service
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class VisitForm(forms.ModelForm):
    current_visit_date = JalaliDateField(
        label="تاریخ ویزیت",
        widget=AdminJalaliDateWidget(
            attrs={
                'class': 'jalali_date-input w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800',
                'placeholder': 'تاریخ ویزیت'
            }
        )
    )
    next_visit_date = JalaliDateField(
        label="تاریخ ویزیت بعدی",
        widget=AdminJalaliDateWidget(
            attrs={
                'class': 'jalali_date-input w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800',
                'placeholder': 'تاریخ ویزیت بعدی'
            }
        )
    )

    class Meta:
        model = Visit
        fields = [
            'first_name',
            'last_name',
            'phone',
            'current_visit_date',
            'next_visit_date',
            'service',
            'SMS_sent'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800 ',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800',
                'placeholder': 'نام خانوادگی'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800',
                'placeholder': 'شماره تلفن'
            }),
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-[#A1A6B4] border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800'
            }),
            'SMS_sent': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }

class AppointmentSearchForm(forms.Form):
    date = JalaliDateField(
        label="تاریخ نوبت",
        required=False,
        widget=AdminJalaliDateWidget(
            attrs={
                'class': 'bg-white jalali_date-input w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-stone-500 text-gray-800',
                'placeholder': 'تاریخ نوبت را وارد کنید...'
            }
        )
    )
