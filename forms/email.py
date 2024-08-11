from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
    
    
def Envoyer_page_html_par_mail(suject, chemin, to, reception_list, domaine, email_new):
    try:
        html_content = render_to_string(chemin, {'to':to,'user_mail':reception_list,'domaine':domaine, 'email':email_new})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            suject,
            text_content,
            settings.EMAIL_HOST_USER,
            [to]
        )
        
        email.attach_alternative(html_content, 'text/html')
        email.send()
        return True
    except Exception as e:
        return print(e, "my error")