# Generated by Django 2.0.3 on 2018-04-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgen', '0024_auto_20180422_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='xdcount',
            name='allow_accuracy',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='allow_error',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Error Value?'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='allow_ms',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='require_accuracy',
            field=models.BooleanField(default=False, help_text='Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.', verbose_name='Require Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='require_error',
            field=models.BooleanField(default=False, help_text='Error margin of measurement, indicating error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e. no error.', verbose_name='Require Error Value?'),
        ),
        migrations.AddField(
            model_name='xdcount',
            name='require_ms',
            field=models.BooleanField(default=False, help_text='MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.', verbose_name='Require Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='allow_accuracy',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='allow_error',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Error Value?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='allow_ms',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='require_accuracy',
            field=models.BooleanField(default=False, help_text='Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.', verbose_name='Require Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='require_error',
            field=models.BooleanField(default=False, help_text='Error margin of measurement, indicating error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e. no error.', verbose_name='Require Error Value?'),
        ),
        migrations.AddField(
            model_name='xdfloat',
            name='require_ms',
            field=models.BooleanField(default=False, help_text='MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.', verbose_name='Require Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='allow_accuracy',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='allow_error',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Error Value?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='allow_ms',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='require_accuracy',
            field=models.BooleanField(default=False, help_text='Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.', verbose_name='Require Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='require_error',
            field=models.BooleanField(default=False, help_text='Error margin of measurement, indicating error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e. no error.', verbose_name='Require Error Value?'),
        ),
        migrations.AddField(
            model_name='xdquantity',
            name='require_ms',
            field=models.BooleanField(default=False, help_text='MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.', verbose_name='Require Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='allow_accuracy',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='allow_error',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Error Value?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='allow_ms',
            field=models.BooleanField(default=False, help_text='Allow a UI component for this element even if it is not required.', verbose_name='Allow Magnitude Status?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='require_accuracy',
            field=models.BooleanField(default=False, help_text='Accuracy of the value in the magnitude attribute in the range 0% to (+/-)100%. A value of 0 means that the accuracy is unknown.', verbose_name='Require Accuracy Value?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='require_error',
            field=models.BooleanField(default=False, help_text='Error margin of measurement, indicating error in the recording method or instrument (+/- %). A logical value of 0 indicates 100% accuracy, i.e. no error.', verbose_name='Require Error Value?'),
        ),
        migrations.AddField(
            model_name='xdratio',
            name='require_ms',
            field=models.BooleanField(default=False, help_text='MagnitudeStatus provides a general indication of the accuracy of the magnitude expressed in the XdQuantified subtypes. Should be used to inform users and not for decision support uses.', verbose_name='Require Magnitude Status?'),
        ),
        migrations.AlterField(
            model_name='attestation',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='dm',
            name='ct_id',
            field=models.CharField(default='cjgasr93400028ql3cb10pdu3', editable=False, help_text='The unique identifier for the DM.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='party',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='units',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdfloat',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='adapter_ctid',
            field=models.CharField(default='cjgasr91l00018ql3l9x65gjm', editable=False, help_text='This UUID is generated for datatype that can be included in a Cluster. It is used to create a specific XdAdapter complexType.', max_length=40, unique=True, verbose_name='CUID'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='ct_id',
            field=models.CharField(default='cjgasr91k00008ql3llrshj4w', editable=False, help_text='The unique identifier for the MC.', max_length=40, unique=True, verbose_name='CUID'),
        ),
    ]
