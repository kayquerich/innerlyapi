# Generated by Django 5.2.3 on 2025-07-05 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('innerlyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autorizacao',
            options={'verbose_name_plural': 'Autorizacoes'},
        ),
        migrations.AlterModelOptions(
            name='profissional',
            options={'verbose_name_plural': 'Profissionais'},
        ),
        migrations.AlterModelOptions(
            name='solicitacao',
            options={'verbose_name_plural': 'Solicitacoes'},
        ),
    ]
