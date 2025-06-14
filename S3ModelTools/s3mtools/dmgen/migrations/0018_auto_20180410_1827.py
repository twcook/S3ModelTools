# Generated by Django 2.0.3 on 2018-04-10 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgen', '0017_auto_20180330_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='attestation',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='audit',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='dm',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='participation',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='party',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='referencerange',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='simplereferencerange',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='units',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdboolean',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdfile',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdinterval',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdlink',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdordinal',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdstring',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AddField(
            model_name='xdtemporal',
            name='app_code',
            field=models.TextField(blank=True, default='', help_text='This is only writable from the DMGEN, not via user input. It contains the code required for each component to create the User App.', null=True, verbose_name='App Code'),
        ),
        migrations.AlterField(
            model_name='attestation',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='dm',
            name='ct_id',
            field=models.CharField(default='cjfu00k7j000216l3b9okzvxb', editable=False, help_text='The unique identifier for the DM.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='party',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='adapter_ctid',
            field=models.CharField(default='cjfu00k63000116l3qu9k980a', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='ct_id',
            field=models.CharField(default='cjfu00k61000016l36hjb55lj', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
    ]
