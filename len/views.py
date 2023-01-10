import io
import json
import xlsxwriter

import sender as sender
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from django.contrib.auth import authenticate, login, logout

from .filters import ContactFilter, ClassFilter
from .forms import *
from .models import *
from .decorators import *


def index(request):
    return render(request, 'len/home.html')


def get_xlsx(request, model, columns, ws_name):
    output = io.BytesIO()

    filename = f'current-report.xlsx'
    workbook = xlsxwriter.Workbook(output, {'in_memory': True, 'default_date_format': 'dd/mm/yy',
                                            'time_format': 'hh:mm:ss'})
    worksheet = workbook.add_worksheet(ws_name)

    row_num = 0
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    print(field for field in columns)
    rows = model.objects.all().order_by(columns[0]).values_list(*columns)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, row[col_num])

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    output.close()

    return response


def get_json(request, items_list, filename):
    serialized_items = serialize('json', items_list)
    print(serialized_items)

    with open(filename, 'w') as f:
        jsoned = json.loads(serialized_items)
        json.dump(jsoned, f, indent=2, ensure_ascii=False)

    response = HttpResponse(serialized_items, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response


@login_required(login_url='login')
def get_clients_xlsx(request):
    columns = ['id', 'name', 'fcs', 'client_type', 'client_status']
    return get_xlsx(request, Clients, columns, ws_name='Клиенты')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def get_clients_json(request):
    clients_list = Clients.objects.all().order_by('id')
    filename = 'clients.json'
    return get_json(request, clients_list, filename)


@login_required(login_url='login')
def get_guests_xlsx(request):
    columns = ['client_id', 'guest_name', 'class_date', 'class_time']
    return get_xlsx(request, model=LastMonthGuests, columns=columns, ws_name='Гости')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def get_guests_json(request):
    guests_list = LastMonthGuests.objects.all().order_by('client_id')
    filename = 'guests.json'
    return get_json(request, guests_list, filename)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['user'])
# def user_page(request):
#     clients = request.user.user.order_set.all()
#
#     print('CLIENTS ', clients)
#     context = {'clients': clients}
#     return render(request, 'len/user.html', context)


class LoginUser(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        form = LoginUserForm
        context = {'form': form}
        return render(request, 'len/login.html', context)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Логин или пароль неверны!')
            context = {}

            return render(request, 'len/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'len/register.html', context)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, 'Пользователь ' + username + ' успешно создан')

            return redirect('login')


class ClientsList(View):
    """Список клиентов"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        contacts = Contacts.objects.all().order_by('id')
        contacts_filter = ContactFilter(request.GET, queryset=contacts)
        clients = []
        if len(contacts_filter.qs) != len(contacts):
            for contact in contacts_filter.qs.all():
                clients.append(contact.client)
        else:
            clients = Clients.objects.all().order_by('id')

        paginator = Paginator(clients, per_page=10)
        page_number = request.GET.get('page', None)
        if not page_number:
            page_number = 1

        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

        context = {'page_obj': page_obj,
                   'contacts_filter': contacts_filter}

        return render(request, 'len/clients.html', context)


class ClientDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        client = Clients.objects.get(id=pk)
        contacts = ClientsContacts.objects.filter(client=client.id)

        context = {'client': client, 'contacts': contacts, 'pk': pk}
        return render(request, 'len/client_card.html', context)


class ClientCreate(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request):
        form = ClientForm()
        context = {'form': form}
        return render(request, 'len/add_client.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('client', pk=client.pk)


class ClientUpdate(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request, pk):
        client = Clients.objects.get(id=pk)
        form = ClientForm(instance=client)
        context = {'form': form}
        return render(request, 'len/update_client.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def post(self, request, pk):
        client = Clients.objects.get(id=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client', pk=client.pk)


class ClientDelete(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['']))
    def get(self, request, pk):
        client = Clients.objects.get(id=pk)
        context = {'client': client, 'pk': pk}
        return render(request, 'len/delete_client.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['']))
    def post(self, request, pk):
        client = Clients.objects.get(id=pk)
        client.delete()
        return redirect('clients')


class ContactsDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        contact = Contacts.objects.get(id=pk)

        context = {'contact': contact, 'pk': pk}
        return render(request, 'len/contact_card.html', context)


class ContactCreate(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request, pk):
        contact_form = ContactForm(prefix="contact")
        type_form = ClientsContactsForm(prefix="type")
        context = {'form': contact_form, 'type_form': type_form, 'pk': pk}
        return render(request, 'len/add_contact.html', context)

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def post(self, request, pk):
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()

        return redirect('client', pk=pk)


class ClassesList(View):
    """Список занятий"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        classes = Classes.objects.all().order_by('id')
        classes_filter = ClassFilter(request.GET, queryset=classes)

        paginator = Paginator(classes_filter.qs, per_page=10)
        page_number = request.GET.get('page', None)
        if not page_number:
            page_number = 1

        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

        context = {'page_obj': page_obj,
                   'classes_filter': classes_filter}

        return render(request, 'len/classes.html', context)


class ClassDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        _class = Classes.objects.get(id=pk)
        guests = Guests.objects.filter(field_class=_class.id)

        context = {'cls': _class, 'guests': guests, 'pk': pk}
        return render(request, 'len/class_card.html', context)


@receiver(post_save, sender=Contacts)
def create_contact(sender, instance, **kwargs):
    first_name = instance.first_name
    last_name = instance.last_name
    middle_name = instance.middle_name
    fcs = f"{last_name} {first_name} {middle_name}"

    Clients.objects.create(name=first_name, fcs=fcs, client_type=1, client_status=5, contacts=instance.id)
