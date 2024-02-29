from django.urls import path

from apps.main.views import author, create, details, index, ProductLikeView, SearchExploreView, \
    ExploreView, product_update, product_delete, ProductListView, CategoryDetailView

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('author', author, name='author'),
    path('create', create, name='create'),
    path('details', details, name='details'),
    path('explore/', ExploreView.as_view(), name="explore"),
    path('product/<pk>', ProductLikeView.as_view(), name='product-like'),
    path('search', SearchExploreView.as_view(), name='search'),
    path('category/<pk>', CategoryDetailView.as_view(), name='category_list'),
    path('item-list/', ProductListView.as_view(), name="item_list"),
    path('update/<int:pk>', product_update, name="update"),
    path('delete/<int:pk>', product_delete, name="delete"),
]
