from jinja2 import Template

def render_template(template_path, context):

    with open(template_path) as f:
        template = Template(f.read())

    return template.render(context)
