# Generated by Django 2.2.3 on 2019-07-11 15:39

from django.db import migrations

def set_display_order(apps, schema_editor):
    cell_order = ['blasts','promyelocytes','myelocytes','meta','neutrophils','monocytes','basophils',
                'eosinophils','lymphocytes','plasma_cells','erythroid','other','lymphoblasts']

    CellType = apps.get_model('main', 'CellType')
    for cell_type in CellType.objects.all():
        cell_type.display_order = cell_order.index(cell_type.machine_name)
        cell_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_add_display_order'),
    ]

    operations = [
        migrations.RunPython(set_display_order),
    ]