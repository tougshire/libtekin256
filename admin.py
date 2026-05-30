from django.contrib import admin

from .models import (
    Article,
    ArticleNote,
    ArticleNoteSubject,
    ArticleSnap,
    Role,
    ArticleStatus,
    Mamodel,
    MamodelCategory,
)


class ArticleNoteSubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_line", "last_used")


admin.site.register(Article)

admin.site.register(ArticleSnap)

admin.site.register(Role)

admin.site.register(ArticleStatus)

admin.site.register(Mamodel)

admin.site.register(MamodelCategory)

admin.site.register(ArticleNote)

admin.site.register(ArticleNoteSubject, ArticleNoteSubjectAdmin)
