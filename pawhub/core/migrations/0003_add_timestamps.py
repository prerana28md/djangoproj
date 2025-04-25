from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20250424_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 