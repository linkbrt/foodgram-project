from django.http.request import HttpRequest


def tags_to_render(request: HttpRequest):
    tags = request.GET.get('tags')
    render_tags = {}
    if tags:
        render_tags = {
            value: 'tags__checkbox_active'
            for value in tags.split(',')
        }
    return {'tags': render_tags}

def purchases_counter(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        return {'counter': user.purchases.count()}
    return {'counter': ''}
