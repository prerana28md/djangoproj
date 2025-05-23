# Generated by Django 5.0.3 on 2025-05-18 12:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('species', models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('fish', 'Fish'), ('reptile', 'Reptile'), ('other', 'Other')], max_length=20)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], max_length=10)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pets/')),
                ('location', models.CharField(blank=True, max_length=200)),
                ('type', models.CharField(choices=[('adoption', 'For Adoption'), ('sale', 'For Sale'), ('exchange', 'For Exchange'), ('lost', 'Lost Pet'), ('found', 'Found Pet')], default='adoption', max_length=20)),
                ('status', models.CharField(choices=[('available', 'Available'), ('pending', 'Pending'), ('adopted', 'Adopted'), ('sold', 'Sold'), ('exchanged', 'Exchanged'), ('returned', 'Returned to Owner')], default='available', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('vaccination', 'Vaccination'), ('checkup', 'Checkup'), ('surgery', 'Surgery'), ('medication', 'Medication'), ('other', 'Other')], max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='health_records/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='pets.pet')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
