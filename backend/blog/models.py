from django.db import models
from home.models import HomePage
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page
from wagtailcodeblock.blocks import CodeBlock


class PostTag(TagBase):
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="250 characters long, can also be used in SEO description for the page",
    )


class TaggedWithPostTags(ItemBase):
    tag = models.ForeignKey(
        PostTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_tags",
    )
    content_object = ParentalKey(
        to="blog.PostPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class CategoryPage(Page):
    description = RichTextField(blank=True)

    content_panels = (
        *Page.content_panels,
        FieldPanel("description"),
        InlinePanel("featured", label="Featured Posts"),
    )

    parent_page_types = (HomePage, "CategoryPage")


class PostPage(Page):
    intro = RichTextField(blank=True)
    body = StreamField(
        (
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code", CodeBlock(label="Code", default_language="python")),
        ),
        use_json_field=True,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    tags = ClusterTaggableManager(through=TaggedWithPostTags, blank=True)

    content_panels = (
        *Page.content_panels,
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
    )

    parent_page_types = (CategoryPage,)


class FeaturedPost(Orderable):
    category = ParentalKey(CategoryPage, on_delete=models.CASCADE, related_name="featured")
    post = models.ForeignKey(PostPage, on_delete=models.CASCADE, related_name="+")
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This image can be different from any images in the post.",
    )
    panels = (
        FieldPanel("post"),
        FieldPanel("preview_image"),
    )
