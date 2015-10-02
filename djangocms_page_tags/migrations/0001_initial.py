# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '__latest__'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('extended_object', models.OneToOneField(to='cms.Page', editable=False)),
                ('public_extension', models.OneToOneField(to='djangocms_page_tags.PageTags', related_name='draft_extension', null=True, editable=False)),
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
                ('extended_object', models.OneToOneField(to='cms.Title', editable=False)),
                ('public_extension', models.OneToOneField(to='djangocms_page_tags.TitleTags', related_name='draft_extension', null=True, editable=False)),
                ('tags', taggit_autosuggest.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
            options={
                'verbose_name': 'Page tags (language-dependent)',
            },
        ),
    ]
