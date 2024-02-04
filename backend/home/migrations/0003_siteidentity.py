# Generated by Django 5.0.1 on 2024-02-03 05:29

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(max_length=100)),
                ('seo_description', models.TextField(blank=True, help_text='Used in SEO meta tags, should be 50-160 characters long')),
                ('seo_keywords', models.CharField(blank=True, help_text="List of words in SEO meta tags, eg 'blog, django, python' without quotes, comma separated", max_length=250)),
                ('footer', wagtail.fields.RichTextField(blank=True)),
                ('info_popup', models.TextField(blank=True, help_text='Adds a message to the top of the site on all pages. Change to blank to remove the message.')),
                ('youtube_url', models.URLField(blank=True)),
                ('youtube_name', models.CharField(blank=True, max_length=100)),
                ('twitter_url', models.URLField(blank=True)),
                ('twitter_name', models.CharField(blank=True, max_length=100)),
                ('favicon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('title_logo', models.ForeignKey(blank=True, help_text='Used for the main top logo', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]