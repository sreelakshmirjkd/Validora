

from django.views import View
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings

from .forms import AppointmentForm


from django.views.generic import TemplateView

from datetime import date
from .models import Appointment
from .utils import get_available_slots_for_date



from django.http import JsonResponse
from datetime import datetime


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .utils import get_available_slots_for_date, is_working_day

 
import gspread
from google.oauth2.service_account import Credentials
from datetime import date, time

from django.core.mail import EmailMultiAlternatives





class ContactView(View):
    form_class = ContactForm
    template_name = 'index.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            subject = f"New message from {name}"
            full_message = f"From: {name} <{email}>\nPhone: {phone}\n\n{message}"

            # --------------------------------------------------------------------


            # try:
            #     append_to_google_sheet([name, email, phone, message])
            # except Exception as e:
            #     # Log error or handle failure but don't crash
            #     print(f"Failed to append to Google Sheet: {e}")


            # # to team

            # send_mail(
            #     subject,
            #     full_message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.V_EMAIL],
            #     fail_silently=False,
            # )

            # confirmation_subject = "We received your message"
            # confirmation_message = (
            # f"Hi {name},\n\n"
            # "Thank you for contacting us. We’ve received your message and will respond shortly.\n\n"
            # "Best regards,\n"
            # "Team"
            # )
        # -----------------------additional to remove later---------------------------------------------

            return render(request, self.template_name, {
                'form': self.form_class(),
                'message': "Form submissions are temporarily paused."
            })
        
        # --------------------------------------------------------------------


            # to customer

        #     send_mail(
        #     confirmation_subject,
        #     confirmation_message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email],  
        #     fail_silently=False,
        #     )

        # return redirect('form_submit')  
        



# contact_form


# def append_to_google_sheet(row):
#     # Path to your service account JSON file
#     SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_FILE

#     # Define the scopes
#     SCOPES = settings.SCOPES

#     creds = Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE,
#         scopes=SCOPES
#     )
     
#     client = gspread.authorize(creds)

#     # Open your spreadsheet by ID
#     SPREADSHEET_ID = settings.GOOGLE_SHEET_ID_CONTACT
#     sheet = client.open_by_key(SPREADSHEET_ID).sheet1  

#     # Append the row
#     sheet.append_row(row)

# --------------------------------------------------------------------



class AppointmentView(View):
    form_class = AppointmentForm
    template_name = 'appointment_form.html'



    def get(self, request):
        form = self.form_class()
        today = date.today()

        booked_times = Appointment.objects.filter(preferred_date=today).values_list('preferred_time', flat=True)
        available_slots = get_available_slots_for_date(today, booked_times)

        two_pm_time = time(14, 0)
        two_pm_str = two_pm_time.strftime("%H:%M:%S")

        if two_pm_time in booked_times:
            # Remove 2 PM if present in available_slots
            available_slots = [slot for slot in available_slots if slot != two_pm_time]
        else:
            # Add 2 PM if not present
            if two_pm_time not in available_slots:
                # Insert at front (so it shows first)
                available_slots.insert(0, two_pm_time)

        return render(request, self.template_name, {
            'form': form,
            'available_slots': available_slots,
            'two_pm_str': two_pm_str,
        })
    




    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save()

    # --------------------------------------------------------------------
    

    #         # Append appointment data to Google Sheet
    #         try:
    #             append_appointment_to_google_sheet(appointment)
    #         except Exception as e:
    #             print(f"Failed to append to Google Sheet: {e}")

    #         subject = 'Appointment Confirmed'
    #         from_email = settings.DEFAULT_FROM_EMAIL
    #         to_email = [appointment.email]

    #         text_content = f"""Dear {appointment.name},

    # Thank you for scheduling an appointment with us. This email is to confirm your appointment as follows:

    # Date: {appointment.preferred_date}
    # Time: {appointment.preferred_time}

    # If you have any questions or need to reschedule, please feel free to reply to this email.

    # We look forward to assisting you.

    # Best regards,
    # Team
    # Validora
    # FDS COOP LLP
    # """

    #         html_content = f"""
    #         <html>
    #         <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    #             <p>Dear {appointment.name},</p>

    #             <p>Thank you for scheduling an appointment with us. This email is to confirm your appointment as follows:</p>

    #             <table style="border-collapse: collapse; margin: 20px 0;">
    #             <tr>
    #                 <td style="padding: 8px; font-weight: bold;">Date:</td>
    #                 <td style="padding: 8px;">{appointment.preferred_date}</td>
    #             </tr>
    #             <tr>
    #                 <td style="padding: 8px; font-weight: bold;">Time:</td>
    #                 <td style="padding: 8px;">{appointment.preferred_time}</td>
    #             </tr>
    #             </table>

    #             <p>If you have any questions or need to reschedule, please feel free to reply to this email.</p>

    #             <p>We look forward to assisting you.</p>

    #             <br>
    #             <p>Best regards,<br>
    #             Team<br>
    #             Validora<br>
    #             FDS COOP LLP</p>
    #         </body>
    #         </html>
    #         """

    #         msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send(fail_silently=False)


    #         # Team notification

    #         send_mail(
    #             'New Appointment Booked',
    #             f'''
    #             Name: {appointment.name}
    #             Email: {appointment.email}
    #             Phone: {appointment.phone}
    #             Visa Country: {appointment.visa_country}
    #             Agency Name: {appointment.agency_name}
    #             Preferred Date: {appointment.preferred_date}
    #             Preferred Time: {appointment.preferred_time}
    #             Confusions: {", ".join([c.name for c in appointment.confusions.all()])}
    #             Notes: {appointment.notes}
    #             ''',
    #             settings.DEFAULT_FROM_EMAIL,
    #             [settings.V_EMAIL],
    #             fail_silently=False,
    #         )

    #         return redirect('appointment_submit')

    #     # If form invalid
    #     return render(request, self.template_name, {'form': form})




# appointment



# def append_appointment_to_google_sheet(appointment):
#     SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_FILE
#     SCOPES = settings.SCOPES

#     creds = Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE,
#         scopes=SCOPES
#     )

#     client = gspread.authorize(creds)
#     SPREADSHEET_ID = settings.GOOGLE_SHEET_ID_APPOINTMENT
#     sheet = client.open_by_key(SPREADSHEET_ID).sheet1

#     # Define headers (ensure this matches your appointment model exactly)
#     headers = [
#         'Name', 'Email', 'Phone', 'Address', 'City', 'State',
#         'Visa Country', 'Agency Name', 'Preferred Date', 'Preferred Time',
#         'Confusions', 'Notes','consent_privacy_policy','consent_terms_conditions', 
#         'Payment Status','file','reviewed','status','Submitted At'
#     ]

#     # Check and add header if not present
#     existing_data = sheet.get_all_values()
#     if not existing_data or existing_data[0] != headers:
#         sheet.insert_row(headers, 1)
#         existing_data = sheet.get_all_values()  # Refresh after inserting header

#     # Prepare new row
#     new_row = [
#         appointment.name,
#         appointment.email,
#         appointment.phone,
#         appointment.address,
#         appointment.city,
#         appointment.state,
#         appointment.visa_country,
#         appointment.agency_name,
#         str(appointment.preferred_date),
#         str(appointment.preferred_time),
#         ", ".join([c.name for c in appointment.confusions.all()]),
#         appointment.notes or '',
#         appointment.consent_privacy_policy,
#         appointment.consent_terms_conditions,
#         appointment.payment_status,
#         appointment.file,
#         appointment.reviewed,
#         appointment.status,
#         str(appointment.submitted_at),
        
        

#     ]

#     # duplication check (based on email + preferred_date)
#     for row in existing_data[1:]:  # Skip header
#         if len(row) >= 10 and row[1] == appointment.email and row[9] == str(appointment.preferred_date):
#             print("Duplicate entry found. Skipping append.")
#             return

#     # Append the row
#     sheet.append_row(new_row)

# --------------------------------------------------------------------






class AppointmentSubmitView(TemplateView):
    template_name = 'appointment_submit.html'


@method_decorator(csrf_exempt, name='dispatch')
class AvailableSlotsView(View):
    def post(self, request):
        date_str = request.POST.get('date')
        if not date_str:
            return JsonResponse({'available_slots': []})

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'available_slots': []})

        if not is_working_day(date_obj):
            return JsonResponse({'available_slots': []})

        available_slots = get_available_slots_for_date(date_obj)
        slots_str = [slot.strftime("%H:%M:%S") for slot in available_slots]
        slots_label = [slot.strftime("%I:%M %p") for slot in available_slots]

        return JsonResponse({
            'available_slots': [{'value': v, 'label': l} for v, l in zip(slots_str, slots_label)]
        })



class PrivacyView(TemplateView):
    template_name = 'privacy.html'



class TermsView(TemplateView):
    template_name = 'terms.html'


