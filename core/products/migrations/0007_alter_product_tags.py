# Generated by Django 5.1.1 on 2025-03-01 13:29

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_alter_product_author_alter_product_category_and_more"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="Use tags to add further categorization to products.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
