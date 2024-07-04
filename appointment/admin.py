from django.contrib import admin
from django.core.mail import send_mail
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.appointment_status == "Running" and obj.appointment_type == "Online":
            send_mail("Appointment is running", "You appointment is running join as soon as possible",
                      "noreply@gmail.com", [obj.patient.user.email])

        return super().save_model(request, obj, form, change)


admin.site.register(Appointment, AppointmentAdmin)
