# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('cms', '0003_auto_20140926_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('extended_object', models.OneToOneField(to='cms.Page', editable=False, on_delete=models.CASCADE)),
                ('public_extension', models.OneToOneField(to='djangocms_page_tags.PageTags', related_name='draft_extension', null=True, editable=False, on_delete=models.CASCADE)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
            options={
                'verbose_name': 'Page tags (all languages)',
            },
        ),
        migrations.CreateModel(
            name='TitleTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('extended_object', models.OneToOneField(to='cms.Title', editable=False, on_delete=models.CASCADE)),
                ('public_extension', models.OneToOneField(to='djangocms_page_tags.TitleTags', related_name='draft_extension', null=True, editable=False, on_delete=models.CASCADE)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
            options={
                'verbose_name': 'Page tags (language-dependent)',
            },
        ),
    ]
