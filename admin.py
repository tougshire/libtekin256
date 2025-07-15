from django.contrib import admin

from .models import Article, ArticleSnap, ArticleCategory, ArticleStatus, Mamodel, MamodelCategory

admin.site.register(Article)

admin.site.register(ArticleSnap)

admin.site.register(ArticleCategory)

admin.site.register(ArticleStatus)

admin.site.register(Mamodel)

admin.site.register(MamodelCategory)
