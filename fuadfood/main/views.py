from ast import Or
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import ItemForm
from .models import OurDishes,Item,Order, Reviews
from django.views.generic import (CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone

def home_view(request):
    productone=OurDishes.objects.get(id=7)
    producttwo=OurDishes.objects.get(id=8)
    productthree=OurDishes.objects.get(id=9)
    context={
        'displayseven':productone,
        'displayeight':producttwo,
        'displaynine':productthree
    }
    return render(request,"main/home.html",context)

def menu_view(request):
    queryset= Item.objects.all() #all products
    context= {
                "object_list":queryset
    }
    return render (request, "main/menu.html", context)

class ItemCreateView(CreateView):
    template_name='main/food_create.html'
    form_class= ItemForm
    queryset= Item.objects.all()
    success_url = '/menu'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class ItemUpdateView(UpdateView):
    template_name='main/food_create.html'
    form_class= ItemForm
    queryset= Item.objects.all()

    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(Item, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)



@login_required
def food_detail_view(request, id):
    queryset=Reviews.objects.filter( item=Item.objects.get(id=id))
    if request.method == "POST":        
        title = request.POST.get('title')
        price = request.POST.get('price')
        portions = request.POST.get('portions')
        Order.objects.create(title=title, price=price, portions=portions, user=request.user)
    try:
        obj = Item.objects.get(id=id)
    except Item.DoesNotExist:
        raise Http404
    context={
        "object": obj,
        "review":queryset
    } 
    return render (request, "main/dishes.html", context)

@login_required
def cart_view(request):
    queryset=Order.objects.filter(user=request.user,ordered=False) 
    cart_items = Order.objects.filter(user=request.user)
    bill = cart_items.aggregate(Sum('price'))
    pieces = cart_items.aggregate(Sum('portions'))
    total = bill.get("price__sum")
    total_pieces = pieces.get("portions__sum")
    context = {
        'object_list':queryset,
        'cart_items':cart_items,
        'total': total,
        'total_pieces': total_pieces,
    }
    return render (request, "main/tray.html",context)

@login_required
def add_reviews(request, id):
    if request.method == "POST":
        user = request.user
        item = Item.objects.get(id=id)
        review = request.POST.get("review")

        reviews = Reviews.objects.create(user=user, item=item, review=review, )
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    #redirect(f"/dishes/{item.id}")
    return render (request, "main/review.html",{})


def delete_order(request, id,):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('cart')

def empty_cart(request):
    queryset=Order.objects.filter(user=request.user)
    queryset.delete()
    return redirect('cart')

@login_required
def order_item(request):
    cart_items = Order.objects.filter(user=request.user,ordered=False)
    ordered_on=timezone.now()
    status=('status')
    cart_items.update(ordered=True,ordered_on=ordered_on,status='Active')
    messages.info(request, "Item Ordered")
    return redirect('order-summary')

@login_required
def order_summary(request):
    queryset = Order.objects.filter(user=request.user, ordered=True,status="Active").order_by('-ordered_on')
    cart_items = Order.objects.filter(user=request.user, ordered=True,status="Delivered").order_by('-ordered_on')
    bill = cart_items.aggregate(Sum('price'))
    pieces = cart_items.aggregate(Sum('portions'))
    total = bill.get("price__sum")
    total_pieces = pieces.get("portions__sum")
    context = {
        'object_list':queryset,
        'cart_items':cart_items,
        'total': total,
        'total_pieces': total_pieces,
    }
    return render(request, 'main/order_summary.html', context)


def search_view(request):
    if request.method=="POST":
        searched = request.POST.get('searched')
        queryset= Item.objects.filter(title__contains=searched)
        context={'searched':searched,
                 'items':queryset}
        return render(request, 'main/search.html', context)
    else:
        return render(request, 'main/search.html',context)

""" class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False """

""" class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/menu'

    def test_func(self, id):
        item = self.get_object(id=id)
        if self.request.user == item.created_by:
            return True
        return False
 """
@login_required(login_url='/accounts/login/')
def admin_view(request):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    cart_items = Order.objects.filter(ordered=True,status="Delivered").order_by('-ordered_on')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

@login_required
def update_status(request, id):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = Order.objects.filter(user=request.user, ordered=True,status="Active",id=id)
    delivery_date=timezone.now()
    if status == 'Delivered':
        cart_items.update(status=status)
    return render(request, 'main/pending_orders.html')

@login_required(login_url='/accounts/login/')
def pending_orders(request):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    items = Order.objects.filter(user=request.user, ordered=True,status="Active").order_by('-ordered_on')
    context = {
        'items':items,
    }
    return render(request, 'main/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponse(status=403)
    cart_items = Order.objects.filter(user=request.user, ordered=True)
    pending_total = Order.objects.filter(user=request.user, ordered=True,status="Active").count()
    completed_total = Order.objects.filter(user=request.user, ordered=True,status="Delivered").count()
    count1 = Order.objects.filter(user=request.user, ordered=True).count()
    count2 = Order.objects.filter(user=request.user, ordered=True).count()
    count3 = Order.objects.filter(user=request.user, ordered=True).count()
    total = Order.objects.filter(user=request.user, ordered=True).aggregate(Sum('price'))
    income = total.get("price__sum")
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
    }
    return render(request, 'main/admin_dashboard.html', context)











#remember we want to add delete reviews, delete items, admin page, order summary then we're pretty much done!!!