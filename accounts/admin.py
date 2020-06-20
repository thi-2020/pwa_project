from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from accounts.models import *
from import_export.admin import ExportActionModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

class UserAdmin(DjangoUserAdmin):
    # list_display = ("id",'email','username','phone','phone_verfied',
    list_display = ("id",'email','username','phone','date_joined','is_staff',)
    # here in fieldsets we add the fields which users can see in admin panel
    fieldsets = (
        (None, {'fields': ('email','username','password','phone')}),
        # ('Personal info', {'fields': ('',)}),
        # ('Permissions', {'fields': ('',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # this field will be asked when creating a user in admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','phone','password1', 'password2','is_staff')}
        ),
    )
    ordering = ('-date_joined',)
    search_fields = ('id','email','username')
    # search_fields = ('id','email','user_profile__phone_number','username')
    
    # def phone(self,obj):
    #     user_profile_obj = obj.user_profile
    #     phone_num = user_profile_obj.phone_number
    #     return phone_num




class UserProfileResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'email'))
    
    class Meta:
        model = UserProfile
        export_order = ('id', 'user', )
        
class UserProfileAdmin(ExportActionModelAdmin):
    list_display = ['id','user',]
    search_fields = ('id','user__email',)
    list_display_links  = ('id','user',)
    resource_class = UserProfileResource


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
    list_display = ['id','sender','receiver',"accepted"]



admin.site.register(User,UserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Invitation,InvitationAdmin)
admin.site.register(Connection,ConnectionAdmin)
