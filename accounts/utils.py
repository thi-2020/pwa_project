import requests
import random
from accounts.models import *
from django.core.mail import send_mail
from django.conf import settings

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view,permission_classes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
class TokenGenerator(PasswordResetTokenGenerator):
      pass

account_activation_token = TokenGenerator() 


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_mail(receiver_email,subject,context,html_address,text_address):

    print("context",context)

    email_html_message = render_to_string(html_address, context)
    email_plaintext_message = render_to_string(text_address, context)
                
    print("receiver_email  is",receiver_email)
    msg = EmailMultiAlternatives(
    (subject),
    email_plaintext_message,
    settings.EMAIL_HOST_USER,
    [receiver_email,],
    )
    msg.attach_alternative(email_html_message, "text/html")
    try:
        mail_send_response = msg.send(fail_silently=False)

        print("mail send response is ",mail_send_response)
        print("sent mail worked thats why came here")
        return {"is_sent":True}

    except Exception as e:
        print("error in sending mail in @284 is",e)
        return {"is_sent":False}






def check_invitaion_validity(sender,email=None,phone=None,index=None):


    to_send = dict()
    user = sender
    errors = dict() 
    is_error = False
    # is_limit_error = False


    # sent_threshold = timezone.now() - timedelta(days = 7)
    # print("sent threshold is ",sent_threshold)
    # count = Invitation.objects.filter(sender_id = user.id).filter(created_at__gt = sent_threshold).count()
    # print("count is ",count)
    # if count >= 3:
    #     errors['limit_error'] = "you have reached your limit of 10 weekly invitations"
    #     is_error = True
    #     is_limit_error = True

    #     to_send = {
    #         "is_error":is_error,
    #         "is_limit_error":is_limit_error,
    #         "index":index,
    #         "error":errors
    #     }

    #     return to_send



    if email is not None:
        qs1 = User.objects.filter(email = email).exists()    
        qs3 = Invitation.objects.filter(receiver_email = email).exists()

        if qs1 is True:
            errors['email'] = "An active user is using this e-mail address"
            is_error = True

        if qs3 is True:
            errors['email'] = "Alreday sent an invitation to this email address"
            is_error = True


    if phone is not None:
        qs2 = User.objects.filter(phone = phone).exists()
        qs4 = Invitation.objects.filter(receiver_phone__contains = phone).exists()

        if qs2 is True:
            errors['phone'] = "An active user is using this phone number"
            is_error = True


        if qs4 is True:
            errors['phone'] = "Alreday sent an invitation to this phone number"
            is_error = True


    to_send = {
        "is_error":is_error,
        "index":index,
        "error":errors
    }

    return to_send




def send_mail_to_invite(sender,email,key,invitation_obj_id):

    invitation_obj = Invitation.objects.get(id=invitation_obj_id)
    print("sender email is",sender.email)
    print("email is",email)
    print("key is",key)

    context = {
            # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
            'username':sender.username,
            'invite_url': "http://localhost:3000/signup/?key={key}".format(key=key),
        }
    print("context",context)

    html_address = 'email/invitation.html'
    text_address = 'email/invitation.txt'
    subject = "Initation to join pwa"
            # to_email = settings.FROM_VERIFICATION_EMAIL_ADDRESS


    response = send_mail(email,subject,context,html_address,text_address)
    print("response is",response)
    if response['is_sent'] is False:
        to_add['error']['email'] = response['msg']
        invitation_obj.delete()


    return response



def mutual_friend_list(user1,user2):

    list1 = Connection.objects.filter(from_user=user1).values_list('to_user',flat=True) 
    list1 = list(list1)   
    # list2 = Connection.objects.filter(receiver = user1).values_list('sender',flat=True)  
    # list2 = list(list2)  
    print("type of list 1 is ",type(list1))
    list_a = list1 
    print("lista is",list_a)
    a_set = set(list_a)
    list3 = Connection.objects.filter(from_user = user2).values_list('to_user',flat=True) 
    list3 = list(list3)   
    # list4 = Connection.objects.filter(receiver = user2).values_list('sender',flat=True)       
    # list4 = list(list4)

    list_b = list3 
    b_set = set(list_b)
    result = (a_set.intersection(b_set))
    result_list = list(result) 
    return result_list


def connection_status(from_user,to_user):

    if Connection.objects.filter(from_user=from_user,to_user=to_user).exists():
        return "connected"
    

    if ConnectionRequest.objects.filter(from_user=from_user,to_user=to_user).exists():
        return "connection request done"

    return "not connected"





