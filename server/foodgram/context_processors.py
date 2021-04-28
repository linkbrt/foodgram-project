from django.http.request import HttpRequest


def tags_to_render(request: HttpRequest):
    tags = request.GET.get('tags')
    if not tags:
        return {'tags': {}}
    render_tags = {value: 'tags__checkbox_active' for value in tags.split(',')}
    return {'tags': render_tags}

def purchases_counter(request: HttpRequest):
    user = request.user
    # purchases_list = user.purchases.values('recipe')
    if user.is_authenticated:
        return {'counter': user.purchases.count()}
    return {'counter': ''}
