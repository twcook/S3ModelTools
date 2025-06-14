# Generated by Django 2.0.5 on 2018-06-15 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmgen', '0026_auto_20180614_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='dm',
            name='acs',
            field=models.ForeignKey(blank=True, help_text='Identifier of externally held access control system. This URI can be an ontology, vocabulary or descriptive document; URI link.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dm_access', to='dmgen.XdLink', verbose_name='ACS ID'),
        ),
        migrations.AlterField(
            model_name='attestation',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='dm',
            name='ct_id',
            field=models.CharField(default='cjifyjmbl0002dml3qjuyvt43', editable=False, help_text='The unique identifier for the DM.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='party',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='adapter_ctid',
            field=models.CharField(default='cjifyjm9p0001dml3fx5rvg0w', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='ct_id',
            field=models.CharField(default='cjifyjm9m0000dml3yjjmoqd9', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
    ]
