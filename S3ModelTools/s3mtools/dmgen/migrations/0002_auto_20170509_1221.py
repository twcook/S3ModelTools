# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attestation',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='attestation',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='audit',
        ),
        migrations.AddField(
            model_name='entry',
            name='audit',
            field=models.ManyToManyField(blank=True, help_text='Audit structure to provide audit trail tracking of information.', null=True, to='dmgen.Audit', verbose_name='audit'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='party',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='party',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='predobj',
            name='po_name',
            field=models.CharField(blank=True, default='', help_text='Enter a human readable name for this Predicate/URI combination. This is only used to aide selection, it is not part of the MC semantics.', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='referencerange',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='simplereferencerange',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='units',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='units',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdboolean',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdcount',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='content_mode',
            field=models.CharField(choices=[('select', 'Select Mode:'), ('url', 'Link via a URL'), ('text', 'Embed a text file'), ('binary', 'Embed a binary file')], default='Select Mode:', help_text='Select how the content will referenced, either via a URL or included in the data instance. Example text is; XML, JSON, SQL, etc. Example binary is; MP3, MP4, PNG, etc.', max_length=6, verbose_name='Content Mode'),
        ),
        migrations.AlterField(
            model_name='xdfile',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdinterval',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdlink',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdordinal',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdquantity',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdratio',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdstring',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='asserts',
            field=models.TextField(blank=True, default='', help_text='Valid XPath 2.0 assert constraint statements that muse evaluate to a boolean. See the documentation for details. One per line.', null=True, verbose_name='asserts'),
        ),
        migrations.AlterField(
            model_name='xdtemporal',
            name='pred_obj',
            field=models.ManyToManyField(help_text='Select or create a new set of RDF Objects as semantic links to define this item.', to='dmgen.PredObj', verbose_name='RDF Object'),
        ),
    ]
