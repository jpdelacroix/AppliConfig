from django.contrib import admin
from .models import Post,Category, Genre, Vitapi

from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin


# Register your models here.

admin.site.site_header = "Version beta v1.0";
admin.site.site_title = "SAS France";
admin.site.index_title = "YAML : Ain’t Markup Language";

'''class CustomMPTTModelAdmin(MPTTModelAdmin):
	mptt_indent_field = "some_node_field"'''

#admin.site.register(Post)
admin.site.register(Category , MPTTModelAdmin)

#admin.site.register(Genre)
admin.site.register(Genre,MPTTModelAdmin)


'''class CustomMpptModelAdmin(MPTTModelAdmin):
	mppt_admin_level_indent = 100'''

admin.site.register(Vitapi,MPTTModelAdmin)






