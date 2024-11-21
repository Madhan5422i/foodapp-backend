from django.contrib import admin
from .models import Explore_menu, item_List, Cart, CartItem, Address,CusUser,UserOrders
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CusUser
from .forms import CusUserChangeForm, CusUserCreationForm

class CusUserAdmin(UserAdmin):
    form = CusUserChangeForm
    add_form = CusUserCreationForm
    list_display = ('email', 'firstname', 'username', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'firstname', 'username', 'password', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstname', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'firstname', 'username')
    ordering = ('email',)

admin.site.register(CusUser, CusUserAdmin)

admin.site.register(Cart)
admin.site.register(Explore_menu)
admin.site.register(item_List)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(UserOrders)