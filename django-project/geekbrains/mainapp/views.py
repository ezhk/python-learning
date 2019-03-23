from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'mainapp/index.html')

def products(request, product_name=None):
    if product_name is not None:
        return render(request, 'mainapp/products/%s.html' % product_name)
    return render(request, 'mainapp/products.html')

def contacts(request):
    return render(request, 'mainapp/contacts.html')
