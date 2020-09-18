from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from accounts.models import *
from import_export.admin import ExportActionModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

class UserAdmin(DjangoUserAdmin):
    # list_display = ("id",'email','username','phone','phone_verfied',
    list_display = ("id",'email','username','phone','date_joined','is_staff','first_name','last_name')
    # here in fieldsets we add the fields which users can see in admin panel
    fieldsets = (
        (None, {'fields': ('email','username','password','phone','first_name','last_name',
        'profile_photo','cover_photo','dob','current_city','no_of_friend','no_of_followers','no_of_following')}),
        # ('Personal info', {'fields': ('',)}),
        # ('Permissions', {'fields': ('',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # this field will be asked when creating a user in admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','first_name','last_name','phone','password1', 'password2','is_staff')}
        ),
    )
    ordering = ('-date_joined',)
    search_fields = ('id','email','username')




    # search_fields = ('id','email','user_profile__phone_number','username')
    
    # def phone(self,obj):
    #     user_profile_obj = obj.user_profile
    #     phone_num = user_profile_obj.phone_number
    #     return phone_num






    # list_display = ['id','wallet',]
    # def bitcoin_balance(self,obj):
    #     user = obj.user
    #     ripple_wallet = RippleWallet.objects.get(user=user)
    #     return ripple_wallet.bitcoin_balance
    # def ripple_balance(self,obj):
    #     user = obj.user
    #     ripple_wallet = RippleWallet.objects.get(user=user)
    
    #     return ripple_wallet.ripple_balance
    # def address(self,obj):
    #     user = obj.user
    #     ripple_wallet = RippleWallet.objects.get(user=user)
    
    #     return ripple_wallet.account_id


class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id','sender','receiver_email',"receiver_phone",'invitation_key',"accepted"]
   

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['id','from_user','to_user',]

class VisibilitySettingsAdmin(admin.ModelAdmin):
    list_display = ['user','who_can_see_your_likes_and_comments',
                    'who_can_see_your_connection_list']


class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['id','from_user','to_user','rejected']



class FollowAdmin(admin.ModelAdmin):
    list_display = ['id','from_user','to_user']

admin.site.register(User,UserAdmin)
admin.site.register(ConnectionRequest,ConnectionRequestAdmin)
admin.site.register(VisibilitySettings,VisibilitySettingsAdmin)

admin.site.register(Invitation,InvitationAdmin)
admin.site.register(Connection,ConnectionAdmin)
admin.site.register(Follow,FollowAdmin)
