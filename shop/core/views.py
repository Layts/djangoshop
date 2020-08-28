from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order, Category
from .forms import ItemForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'index.html', context)


# def box(request):
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     context = {
#         'items': Item.objects.all()
#     }
#     print(order_qs[0].items.objects.all())
#     return render(request, 'cart.html', context)
#

def manage_items(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'management.html', context)


def item_new(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ItemForm()
    return render(request, 'management.html', {'form': form})


def add_to_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.create(
            item=item,
            order_name=order)
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order.items.get(item__slug=item.slug).quantity += 1
            order.items.get(item__slug=item.slug).save()
            messages.info(request, "This item quantity was updated.")
            return redirect("/")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("/")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.session.session_key, ordered_date=ordered_date)
        order_item = OrderItem.objects.create(
            item=item,
            order_name=order)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("/")


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:view_items")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


# TODO сделать заебись
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.session.session_key, ordered=False)
            context = {
                'items': order.items.filter()
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "item.html"


class Items(View):
    cat = 'Категория'

    def get(self, *args, **kwargs):
        print(self.request.session.session_key)
        context = {
            'items': Item.objects.filter(category=Category.objects.get(title=self.cat))
        }
        return render(self.request, 'products.html', context)


class Candle(Items):
    cat = 'Свеча'


class Dif(Items):
    cat = 'Диффузор'


class AutoDif(Items):
    cat = 'Авто Диффузор'
