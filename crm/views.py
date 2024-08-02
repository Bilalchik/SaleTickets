from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render
from product.models import Order


@user_passes_test(lambda u: u.is_admin or u.status == 3, login_url='index')
def order_list_view(request):
    orders = Order.objects.all().order_by('-id')

    income = orders.aggregate(total=Sum('total_price'))['total']

    print(income)

    return render(
        request=request,
        template_name='crm/order_list.html',
        context={
            'orders': orders,
            'income': income
        }
    )




