# Generated by Django 3.1 on 2020-10-26 16:06

from django.db import migrations, models
import django.db.models.deletion
import json


def populate_foreign_keys(apps, schema_editor):
    individual_model = apps.get_model("fms_core", "individual")
    sample_model = apps.get_model("fms_core", "sample")
    version_model = apps.get_model("reversion", "Version")
    all_individual_labels = set(individual_model.objects.all().values_list("label", flat=True))
    label_id_map = dict(individual_model.objects.all().values_list("label", "id"))

    # update the sample and individual FKs
    for sample in sample_model.objects.all():
        sample.individual_new = label_id_map.get(sample.individual)
        sample.save()
    for individual in individual_model.objects.all():
        if individual.mother:
            individual.mother_new = label_id_map.get(individual.mother)
        if individual.father:
            individual.father_new = label_id_map.get(individual.father)
        individual.save()

    # update the version id to maintain old data with new structure
    for version in version_model.objects.filter(content_type__model="individual", object_id__in=all_individual_labels):
        label = version.object_id
        # Convert label to id
        version.object_id = label_id_map.get(label)
        # Re-serialize data to fit new model
        data = json.loads(version.serialized_data)
        data[0]["pk"] = version.object_id
        data[0]["fields"]["label"] = label
        data[0]["fields"]["mother"] = label_id_map.get(data[0]["fields"]["mother"])
        data[0]["fields"]["father"] = label_id_map.get(data[0]["fields"]["father"])
        version.serialized_data = json.dumps(data)
        # Save to database
        version.save()

    for version in version_model.objects.filter(content_type__model="sample"):
        # Fix old references to individual from samples
        data = json.loads(version.serialized_data)
        data[0]["fields"]["individual"] = label_id_map.get(data[0]["fields"]["individual"])
        version.serialized_data = json.dumps(data)
        # Save to database
        version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('fms_core', '0007_v2_3_0'),
    ]

    operations = [
        migrations.RenameField(
            model_name='individual',
            old_name='id',
            new_name='label',
        ),
        migrations.AlterField(
            model_name='individual',
            name='father',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Father of the individual.'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='mother',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Mother of the individual.'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='individual',
            field=models.CharField(max_length=200, help_text='Individual associated with the sample.'),
        ),
        migrations.RunSQL(
            "ALTER TABLE fms_core_individual DROP CONSTRAINT fms_core_individual_pkey",
            "ALTER TABLE fms_core_individual_temp ADD PRIMARY KEY (label)"
        ),
        migrations.RunSQL(
            "CREATE TABLE fms_core_individual_temp AS TABLE fms_core_individual",
            "DROP TABLE fms_core_individual_temp"
        ),
        migrations.RunSQL(
            "DROP TABLE fms_core_individual",
            migrations.RunSQL.noop
        ),
        migrations.RunSQL(
            "CREATE TABLE fms_core_individual AS TABLE fms_core_individual_temp WITH NO DATA",
            migrations.RunSQL.noop
        ),
        migrations.AddField(
            model_name='individual',
            name='id',
            field=models.AutoField(primary_key=True, unique=True, blank=False, null=False),
        ),
        migrations.RunSQL(
            "INSERT INTO fms_core_individual SELECT * FROM fms_core_individual_temp",
            migrations.RunSQL.noop
        ),
        migrations.RunSQL(
            "DROP TABLE fms_core_individual_temp",
            migrations.RunSQL.noop
        ),
        migrations.AddField(
            model_name='sample',
            name='individual_new',
            field=models.IntegerField(blank=True, null=True, help_text='Individual associated with the sample.'),
        ),
        migrations.AddField(
            model_name='individual',
            name='mother_new',
            field=models.IntegerField(blank=True, null=True, help_text='Mother of the individual.'),
        ),
        migrations.AddField(
            model_name='individual',
            name='father_new',
            field=models.IntegerField(blank=True, null=True, help_text='Father of the individual.'),
        ),
        migrations.RunPython(
            populate_foreign_keys,
            migrations.RunPython.noop
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='individual',
            new_name='individual_old',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='individual_new',
            new_name='individual_id',
        ),
        migrations.RenameField(
            model_name='individual',
            old_name='mother',
            new_name='mother_old',
        ),
        migrations.RenameField(
            model_name='individual',
            old_name='mother_new',
            new_name='mother_id',
        ),
        migrations.RenameField(
            model_name='individual',
            old_name='father',
            new_name='father_old',
        ),
        migrations.RenameField(
            model_name='individual',
            old_name='father_new',
            new_name='father_id',
        ),
        migrations.RunSQL(
            "ALTER TABLE fms_core_sample ADD CONSTRAINT fk_individual FOREIGN KEY (individual_id) REFERENCES fms_core_individual(id)",
            "ALTER TABLE fms_core_sample DROP CONSTRAINT fk_individual;"
        ),
        migrations.RunSQL(
            "ALTER TABLE fms_core_individual ADD CONSTRAINT fk_mother FOREIGN KEY (mother_id) REFERENCES fms_core_individual(id)",
            "ALTER TABLE fms_core_individual DROP CONSTRAINT fk_mother;"
        ),
        migrations.RunSQL(
            "ALTER TABLE fms_core_individual ADD CONSTRAINT fk_father FOREIGN KEY (father_id) REFERENCES fms_core_individual(id)",
            "ALTER TABLE fms_core_individual DROP CONSTRAINT fk_father;"
        ),
        migrations.RemoveField(
            model_name='individual',
            name='father_old',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='mother_old',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='individual_old',
        ),
    ]
