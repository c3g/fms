# Generated by Django 3.0.6 on 2020-05-22 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fms_core', '0001_v1_0_0'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='kind',
            field=models.CharField(choices=[('96-well plate', '96-well plate'), ('384-well plate', '384-well plate'), ('tube', 'tube'), ('tube box 8x8', 'tube box 8x8'), ('tube box 9x9', 'tube box 9x9'), ('tube box 10x10', 'tube box 10x10'), ('tube rack 8x12', 'tube rack 8x12'), ('drawer', 'drawer'), ('freezer rack 4x4', 'freezer rack 4x4'), ('freezer rack 7x4', 'freezer rack 7x4'), ('freezer rack 8x6', 'freezer rack 8x6'), ('freezer rack 11x6', 'freezer rack 11x6'), ('freezer 3 shelves', 'freezer 3 shelves'), ('freezer 5 shelves', 'freezer 5 shelves'), ('room', 'room'), ('box', 'box')], help_text='What kind of container this is. Dictates the coordinate system and other container-specific properties.', max_length=20),
        ),
        migrations.AlterField(
            model_name='container',
            name='location',
            field=models.ForeignKey(blank=True, help_text='An existing (parent) container this container is located inside of.', limit_choices_to={'kind__in': ('tube box 8x8', 'tube box 9x9', 'tube box 10x10', 'tube rack 8x12', 'drawer', 'freezer rack 4x4', 'freezer rack 7x4', 'freezer rack 8x6', 'freezer rack 11x6', 'freezer 3 shelves', 'freezer 5 shelves', 'room', 'box')}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='fms_core.Container'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='taxon',
            field=models.CharField(choices=[('Homo sapiens', 'Homo sapiens'), ('Mus musculus', 'Mus musculus'), ('Sars-Cov-2', 'Sars-Cov-2')], help_text='Taxonomic group of a species.', max_length=20),
        ),
    ]