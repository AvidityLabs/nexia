from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_to_user(email: str):
    subject = 'Welcome to [Your Company Name]'
    template = 'emails/registration_email.html'  # Path to the HTML email template
    from_email = 'aviditylabs@hotmail.com'
    recipient_list = [email]  # Replace with the recipient's email address
    
    # Generate the HTML content of the email using the template
    context = {
        'user_name': 'John Doe',  # Replace with the user's name
        'dashboard_link': 'https://www.example.com/dashboard'  # Replace with the actual dashboard URL
    }
    html_message = render_to_string(template, context)
    
    # Generate the plain text version of the email
    plain_message = strip_tags(html_message)
    
    # Send the email
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)