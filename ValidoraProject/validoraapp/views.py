from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm

class ContactFormView(FormView):
    template_name = 'index.html'           # Your HTML template
    form_class = ContactForm                   # The form to use
    success_url = reverse_lazy('home')         # Redirect after success

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you! Your message has been submitted.")
        return super().form_valid(form)
