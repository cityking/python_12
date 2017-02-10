from django.contrib import admin
from .models import User,Ad, Category, Tag, Article, Links, Comment 

# Register your models here.
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
#admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'js/editor/kindeditor-4.1.10/kindeditor-all.js',
            'js/editor/kindeditor-4.1.10/lang.zh_CN.js',
            'js/editor/kindeditor-4.1.10/config.js',
        )
admin.site.register(Links)
admin.site.register(Comment)
