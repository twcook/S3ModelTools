# Generated by Django 2.0.3 on 2018-03-25 22:07

import cuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgen', '0010_auto_20180325_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attestation',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='party',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='adapter_cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='cuid',
            field=models.CharField(default=cuid.cuid, editable=False, help_text='The unique identifier for the MC.', max_length=40, verbose_name='CUID'),
        ),
    ]