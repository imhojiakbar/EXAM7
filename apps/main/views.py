import datetime
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from apps.main.forms import ProductCreateForm, ProductUpdateForm
from apps.main.models import Product, Category


def index(request):
    # return render(request, 'index.html')
    if request.user.is_authenticated:
        posts = Product.objects.exclude(author=request.user).filter().order_by("created_at")
    else:
        posts = Product.objects.all().filter().order_by("created_at")
    size = request.GET.get("size", 4)
    page = request.GET.get("page", 1)
    paginator = Paginator(posts, size)
    page_obj = paginator.page(page)
    return render(request, "main/index.html", context={"page_obj": page_obj, "num_pages": paginator.num_pages})


def author(request):
    return render(request, 'main/author.html')


def create(request):
    return render(request, 'main/create.html')


def details(request):
    return render(request, 'main/details.html')


class CategoryDetailView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        items = sorted(Product.objects.filter(category=category), key=lambda o: o.like_count, reverse=True)
        context = {
            "category": category,
            "items": items,
       }
        return render(request, "category_list.html", context=context)



class ProductListView(View):
    def get(self, request):
        items = Product.objects.all()
        context = {
            "items": items,
        }
        return render(request, "items_list.html", context=context)


class ProductLikeView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)


class ExploreView(View):
    model = Product
    def get(self, request):
        items = Product.objects.all()
        size = request.GET.get("size", 4)
        page = request.GET.get("page", 1)
        paginator = Paginator(items, size)
        page_obj = paginator.page(page)
        return render(request, "main/explore.html", context={'items': items,"page_obj": page_obj, "num_pages": paginator.num_pages})


class SearchExploreView(View):
    def get(self, request):
        q = request.GET.get('q', None)
        if q:
            items = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        else:
            items = None

        context = {
            'param': q,
            'items': items
        }
        return render(request, 'search.html', context=context)


@login_required()
def post_create(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            item = Product(title=form.cleaned_data["title"], description=form.cleaned_data["description"],
                        category=form.cleaned_data["category"], ends_in=form.cleaned_data["ends_in"],
                        price=form.cleaned_data["price"],owner=form.cleaned_data["owner"],
                        image=form.cleaned_data["image"],
                        author=request.user)
            # item.author = request.user
            item.save()
            messages.success(request, "item successfully created")
            return redirect(reverse('main:author', kwargs={"username": request.user.username}))
        else:
            return render(request, "main/create.html", {"form": form})
    else:
        form = ProductCreateForm()
        return render(request, "main/create.html", {"form": form})


@login_required()
def product_update(request, pk: int):
    item = Product.objects.get(pk=pk)
    if request.method == "POST":
        form = ProductUpdateForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "product successfully updated")
            return redirect(reverse('main:details', kwargs={"pk": item.id}))
        else:
            return render(request, "item_update.html", {"form": form})
    else:
        form = ProductUpdateForm(instance=item)
        return render(request, "item_update.html", {"form": form})


@login_required()
def product_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        messages.success(request, "item successfully deleted")
        item.delete()
        return redirect(reverse('main:author', kwargs={"username": request.user.username}))
    else:
        return render(request, "item_delete.html", {"item": item})