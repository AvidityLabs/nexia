from django.core.mail import send_mail

def send_email_to_user(email: str):
    subject = 'Welcome to My Website'
    message = 'Thank you for signing up. We hope you enjoy our website.'
    from_email = 'mtphlp@gmail.com'
    recipient_list = [email]  # Replace with the recipient's email address
    
    send_mail(subject, message, from_email, recipient_list)