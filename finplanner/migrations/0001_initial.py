# Generated by Django 2.1.3 on 2018-11-11 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('budget', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=1000, null=True)),
                ('type', models.CharField(max_length=30)),
                ('category', models.CharField(choices=[('Accomodation', 'Accomodation'), ('Food', 'Food'), ('Groceries', 'Groceries'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment')], default='', max_length=80)),
                ('payment', models.CharField(max_length=30)),
                ('amount', models.FloatField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.TimeField()),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='finplanner.Account')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
                'ordering': ['-id'],
            },
        ),
    ]