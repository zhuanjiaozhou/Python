from django.contrib import admin


from .models import Host, Position, Operate, User

class OperateInline(admin.StackedInline):
    model = Operate
    extra = 0


class HostAdmin(admin.ModelAdmin):
    inlines = [
        OperateInline,
    ]
    fieldsets = [
        ('server name',  {'fields' : ['hostname']}),
        ('server ip',   {'fields':['ipaddress01','ipaddress02','vip']}),
        ('comment',{'fields':['remark']})
    ]
    list_display = ('hostname','ipaddress01','ipaddress02','vip')

class PositionAdmin(admin.ModelAdmin):
    inlines = [
        OperateInline,
    ]

class UserAdmin(admin.ModelAdmin):
    inlines = [
        OperateInline,
    ]

admin.site.register(Position,PositionAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(User,UserAdmin)
# admin.site.register(Host,HostAdmin)

