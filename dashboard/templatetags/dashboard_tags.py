import ast

from django import template

register = template.Library()


@register.filter(name='addattrs')
def addattrs(field, attrs):
    """
    Appends unlimited number of attributes to html elements.
    Example usage:
    {{ form.username | addattrs:"{'class':'form-control my-username-field-css', 'id': 'id_username'}" }}

    :param field: HTML element that filter tag will be used on
    :param attrs: a list of attributes to be added to html element.
    Takes a string representation of a dict, for example: "{'class':'form-control', 'id':'my-id'}"

    :return: html element with appended attributes
    """

    parsed_attrs = ast.literal_eval(attrs)

    return field.as_widget(attrs=parsed_attrs)
