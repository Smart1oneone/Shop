from .models import Category

def categories(request):
    """
    Return a dictionary containing all top-level categories.

    Parameters:
    - request: HttpRequest object representing the current request.

    Returns:
    - A dictionary with a key 'categories' containing all top-level Category instances where the parent is None.

    """

    categories = Category.objects.filter(parent=None)
    return {'categories': categories}