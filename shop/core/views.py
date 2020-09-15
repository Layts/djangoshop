from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order, Category
from .forms import ItemForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View


def index(request):
    if request.method == "POST":
        item = Item()
        item.title = request.POST.get("name")
        item.price = request.POST.get("age")
        item.save()
        return render(request, "management.html", {"form": userform})
    else:
        userform = ItemForm()
        return render(request, "management.html", {"form": userform})


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'index.html', context)


# class UpdateCrudItem(View):
#
#     def get(self, request):
#         id1 = request.GET.get('id', None)
#         name1 = request.GET.get('name', None)
#         address1 = request.GET.get('address', None)
#         age1 = request.GET.get('age', None)
#
#         obj = Item.objects.get(id=id1)
#         obj.name = name1
#         obj.address = address1
#         obj.age = age1
#         obj.save()
#
#         user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}
#
#         data = {
#             'user': user
#         }
#         return JsonResponse(data)


class ItemView(ListView):
    model = Item
    template_name = 'management.html'
    context_object_name = 'items'


# class CreateCrudItem(View):
#
#     def post(self, request):
#         title = 'sdfsdf'
#         print(title)
#         cat = request.GET.get('cat', None)
#         price = request.GET.get('price', None)
#         obj = Item.objects.create(
#             title=title,
#             price=price,
#             category=cat
#         )
#
#         item = {'id':obj.id,'name':obj.title,'price':obj.price, 'cat': obj.category}
#
#         data = {
#             'item': item
#         }
#         return JsonResponse(data)
#
#
# class DeleteCrudItem(View):
#
#     def get(self, request):
#         title = 'sdfsdf'
#         print(title)
#         cat = request.GET.get('cat', None)
#         price = request.GET.get('price', None)
#         obj = Item.objects.create(
#                 title=title,
#                 price=price,
#                 category=cat
#             )
#
#         item = {'id': obj.id, 'name': obj.title, 'price': obj.price, 'cat': obj.category}
#
#         data = {
#                 'item': item
#             }
#         return JsonResponse(data)

# TODO сделать норм редиректы
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    try:
        request.session['order']
        try:
            quantity = request.session['order'][item.slug]
            request.session['order'][item.slug] = quantity+1
            request.session.modified = True
            return redirect('/')
        except KeyError:
            request.session['order'][item.slug] = 1
            request.session.modified = True
            return redirect('/')
    except KeyError:
        request.session['order'][item.slug] = 1
        return redirect('/')


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
            items = [[get_object_or_404(Item, slug=i), self.request.session['order'][i]] for i in self.request.session['order'].keys()]
            context = {
                'items': items
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
