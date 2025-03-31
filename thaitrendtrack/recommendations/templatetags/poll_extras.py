from django import template

register = template.Library()


@register.filter
def get_percentage(vote_percentages, choice):
    return vote_percentages.get(choice, 0)
