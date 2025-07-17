from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'libtekin256'
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("libtekin256:article-list"))),
    path("article/create/", views.ArticleCreateView.as_view(), name="article-create"),
    path("article/update/<int:pk>/", views.ArticleUpdateView.as_view(), name="article-update"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("article/delete/<int:pk>/", views.ArticleDeleteView.as_view(), name="article-delete"),
    path("articles/", views.ArticleListView.as_view(), name="article-list"),
    path("article/copy/<int:pk>/", views.ArticleCopyView.as_view(), name="article-copy"),
    path("article/filterstore/<int:from_store>/",views.ArticleListView.as_view(), name="article-filterstore"),
    path("rolecreate/", views.RoleCreateView.as_view(), name="role-create"),
    path("rolepopup/", views.RoleCreateView.as_view(), name="role-popup"),
    path("location/create/", views.LocationCreateView.as_view(), name="location-create"),
    path("location/update/<int:pk>/", views.LocationUpdateView.as_view(), name="location-update"),
    path("location/<int:pk>/", views.LocationDetailView.as_view(), name="location-detail"),
    path("location/delete/<int:pk>/", views.LocationDeleteView.as_view(), name="location-delete"),
    path("locations/", views.LocationListView.as_view(), name="location-list"),
    path("location/popup/", views.LocationCreateView.as_view(), name="location-popup"),
    path("model/create/", views.MamodelCreateView.as_view(), name="mamodel-create"),
    path("model/update/<int:pk>/", views.MamodelUpdateView.as_view(), name="mamodel-update"),
    path("model/<int:pk>/", views.MamodelDetailView.as_view(), name="mamodel-detail"),
    path("model/delete/<int:pk>/", views.MamodelDeleteView.as_view(), name="mamodel-delete"),   
    path("model/list/", views.MamodelListView.as_view(), name="mamodel-list"),
    path("model/popup/", views.MamodelCreateView.as_view(), name="mamodel-popup"),
    path("modelcategorycreate/", views.MamodelCategoryCreateView.as_view(), name="mamodelcategory-create"),
    # path("modelcategoryupdate/<int:pk>/", views.MamodelCategoryUpdateView.as_view(), name="mamodelcategory-update"),
    path("modelcategory<int:pk>/", views.MamodelCategoryDetailView.as_view(), name="mamodelcategory-detail"),
    # path("modelcategorydelete/<int:pk>/", views.MamodelCategoryDeleteView.as_view(), name="mamodelcategory-delete"),
    # path("modelcategorylist/", views.MamodelCategoryListView.as_view(), name="mamodelcategory-list"),
    path("modelcategorypopup/", views.MamodelCategoryCreateView.as_view(), name="mamodelcategory-popup"),
    path("articlenotesubject/create/", views.ArticleNoteSubjectCreateView.as_view(), name="articlenotesubject-create"),
    path("articlenotesubject/popup/", views.ArticleNoteSubjectCreateView.as_view(), name="articlenotesubject-popup")



]
