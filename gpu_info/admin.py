import json

from django.contrib import admin
from .models import GPUServer, GPUInfo


class GPUInfoInline(admin.TabularInline):
    model = GPUInfo
    fields = ('index', 'name', 'utilization', 'memory_usage', 'server', 'free', 'complete_free', 'update_at')
    readonly_fields = ('index', 'name', 'utilization', 'memory_usage', 'server', 'free', 'complete_free', 'update_at')

    show_change_link = True

    def memory_usage(self, obj):
        memory_total = obj.memory_total
        memory_used = obj.memory_used
        return '{:d} / {:d} MB ({:.0f}%)'.format(memory_used, memory_total, memory_used / memory_total * 100)

    memory_usage.short_description = '显存占用率'

    def get_extra(self, request, obj, **kwargs):
        return 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


@admin.register(GPUServer)
class GPUServerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'hostname', 'valid', 'can_use')
    list_editable = ('can_use',)
    search_fields = ('ip', 'hostname', 'valid', 'can_use')
    list_display_links = ('ip',)
    inlines = (GPUInfoInline,)
    ordering = ('ip',)
    readonly_fields = ('hostname',)

    class Media:
        # custom css
        css = {
            'all': ('css/admin/custom.css', )
        }

    def has_add_permission(self, request):
        return request.user.is_superuser


@admin.register(GPUInfo)
class GPUInfoAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'utilization', 'memory_usage', 'server', 'usernames', 'free', 'complete_free', 'update_at')
    list_filter = ('server', 'name', 'free', 'complete_free')
    search_fields = ('uuid', 'name', 'memory_used', 'server',)
    list_display_links = ('name',)
    ordering = ('server', 'index')
    readonly_fields = ('uuid', 'name', 'index', 'utilization', 'memory_total', 'memory_used','server', 'processes', 'free', 'complete_free', 'update_at')

    def usernames(self, obj):
        if obj.processes != '':
            arr = obj.processes.split('\n')
            # only show first two usernames
            username_arr = [json.loads(item)['username'] for item in arr[:2]]
            res = ', '.join(username_arr)
            # others use ... to note
            if len(arr) > 2:
                res = res + '...'
            return res
        else:
            return '-'

    def has_add_permission(self, request):
        return False

    def memory_usage(self, obj):
        memory_total = obj.memory_total
        memory_used = obj.memory_used
        return '{:d} / {:d} MB ({:.0f}%)'.format(memory_used, memory_total, memory_used / memory_total * 100)
    
    memory_usage.short_description = '显存占用率'
    usernames.short_description = '占用者'
