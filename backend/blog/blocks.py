from wagtail import blocks

from .models import FeaturedPost, PostPage


class FeaturedPostsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        help_text="If no heading is provided, 'Featured Posts' will be used.",
        required=False,
    )

    def get_featured_posts(self):
        return FeaturedPost.live.order_by("-post__first_published_at")[:5]

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["featured_posts"] = self.get_featured_posts()
        return context

    class Meta:
        label = "Featured Posts"
        template = "blog/blocks/featured_posts_block.html"
        group = "Blog blocks"


class LatestPostsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        help_text="If no heading is provided, 'Latest Posts' will be used.",
        required=False,
    )

    def get_latest_posts(self):
        return PostPage.objects.live().order_by("-first_published_at")[:20]

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["latest_posts"] = self.get_latest_posts()
        return context

    class Meta:
        label = "Latest Posts"
        template = "blog/blocks/latest_posts_block.html"
        group = "Blog blocks"
