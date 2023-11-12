# Generated by Django 4.2.5 on 2023-11-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='obra',
            name='category',
            field=models.CharField(choices=[('Naturaleza muerta', 'Naturaleza Muerta'), ('Retrato', 'Retrato'), ('Paisaje', 'Paisaje'), ('Abstracto', 'Abstracto'), ('Figurativo', 'Figurativo')], default='Naturaleza muerta', max_length=100),
        ),
    ]
