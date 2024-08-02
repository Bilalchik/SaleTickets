from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView


from .models import Ticket, Order
from user.forms import UserRegisterForm
from .filters import TicketFilter

User = get_user_model()


def index_view(request):

    tickets = Ticket.objects.filter(is_active=True)[::-1][:2]

    register_form = UserRegisterForm()

    return render(
        request=request,
        template_name='product/index.html',
        context={
            'tickets': tickets,
            'register_form': register_form
        }
    )


def event_detail_view(request, pk):

    event = get_object_or_404(Ticket, id=pk)

    if request.method == 'POST':
        quantity = request.POST['quantity']

        event_total = event.price * int(quantity)

        current_user = User.objects.get(id=request.user.id)

        if event_total <= current_user.wallet:

            order = Order(
                user=request.user,
                ticket=event,
                quantity=quantity,
                total_price=event_total
            )
            order.save()

            current_user.wallet -= event_total
            current_user.save()

            messages.success(request, 'Билет успешно куплен')
            print('ggg')

        else:
            messages.error(request, 'У вас недостаточно средст')
            print('lol')

    return render(
        request=request,
        template_name='product/event-detail.html',
        context={
            'event': event
        }
    )


def user_profile_view(request):

    user = get_object_or_404(User, id=request.user.id)

    return render(
        request=request,
        template_name='product/profile.html',
        context={
            'user': user
        }
    )


def event_list_view(request):
    event_filter = TicketFilter(request.GET, queryset=Ticket.objects.filter(is_active=True))

    events = event_filter.qs

    if 'search' in request.GET:
        search = request.GET['search']
        events = events.filter(Q(title__iregex=search) | Q(description__iregex=search))

    paginator = Paginator(events, 1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(
        request=request,
        template_name='product/event-listing.html',
        context={
            'events': events,
            'filter': event_filter,
            'page_obj': page_obj
        }
    )


def event_create_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему.')
        return redirect('index')

    elif request.user.status != 2 and request.user.is_admin == False:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('index')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        logo = request.FILES['logo']
        event_date = request.POST['event_date']
        duration = request.POST['duration']
        location = request.POST['location']
        quantity = request.POST['quantity']

        ticket = Ticket(
            title=title,
            description=description,
            price=price,
            logo=logo,
            event_date=event_date,
            duration=duration,
            location=location,
            quantity=quantity
        )

        ticket.save()
        messages.success(request, 'Мероприятие успешно создано.')
        return redirect('index')

    return render(
        request=request,
        template_name='product/event_create.html'
    )


class EventListView(ListView):
    queryset = Ticket.objects.filter(is_active=True)
    template_name = 'product/generic-test.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.all()

        context['orders'] = orders

        return context



class EventDetailView(DetailView):
    model = Ticket
    template_name = 'product/test-detail.html'
    context_object_name = 'event'




