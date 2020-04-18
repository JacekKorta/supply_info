from django.contrib import admin
from info_channel.models import Post, PostBodyParagraph


class PostBodyParagraphInline(admin.StackedInline):
    model = PostBodyParagraph
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'category', 'status')
    list_filter = ('status', 'category', 'publish', 'created', 'author')
    search_fields = ('title',)
    readonly_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    inlines = [PostBodyParagraphInline]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
