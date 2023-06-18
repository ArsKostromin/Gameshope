from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Publisher, St
from .models import Genre

class StAdmin (admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'img', 'published', 'publisher')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content',)
'''
    def image_show(self, obj):
        if obj.img:
            return mark_safe('<img src="{{ st.img }}" with=60 />' .format(obj.img.url))
        return 'None'
'''

class StInstanceAdmin(admin.ModelAdmin):

    list_filter = ('publisher, genre')

'''
    fieldsets = (
        (None, {
            'fields': ('title')
        }),
        ('Availability', {
            'fields': ('buyer')
        }),
    )
'''
admin.site.register(St, StAdmin)
admin.site.register(Genre)
admin.site.register(Publisher)

