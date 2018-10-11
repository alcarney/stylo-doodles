import markdown
from jinja2 import Environment, FileSystemLoader

TEMPLATE_ENV = Environment(
    loader = FileSystemLoader("templates")
)

def render_template(name, context):

    template = TEMPLATE_ENV.get_template(name)
    return template.render(context)


def render_markdown(text):
    """Given some markdown text, render it as html."""
    return markdown.markdown(text)
