from django.contrib import admin
from .models import User, Points, Troops, Cooldown, PowerUp, HourlyFp, Room, Notif
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class PointsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Points, PointsAdmin)

class TroopsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Troops, TroopsAdmin)

class CooldownAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cooldown, CooldownAdmin)

class PowerUpAdmin(admin.ModelAdmin):
    pass
admin.site.register(PowerUp, PowerUpAdmin)

class HourlyFpAdmin(admin.ModelAdmin):
    pass
admin.site.register(HourlyFp, HourlyFpAdmin)

class RoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room, RoomAdmin)

class NotifAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notif, NotifAdmin)
