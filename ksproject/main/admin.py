from django.contrib import admin
from board.models import Post, Comment,Category,Mini_Category
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin 






class PostAdmin(ImportExportMixin,SummernoteModelAdmin,):           
   summernote_field = ('content',)

admin.site.register(Post,PostAdmin)


admin.site.register(Comment)

admin.site.register(Mini_Category)

admin.site.register(Category)