# Generated by Django 4.1.3 on 2023-01-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('len', '0004_delete_clientsgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientsGroup',
            fields=[
                ('is_leader', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Группа клиентов',
                'verbose_name_plural': 'Группы клиентов',
                'db_table': 'clients_group',
                'managed': False,
            },
        ),
    ]
