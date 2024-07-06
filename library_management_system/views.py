from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from Books.models import BookModel,Category
from users.models import Deposite

class home(TemplateView):
    template_name='base.html'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        categorys=Category.objects.all()
        books=BookModel.objects.all()
        slug=self.kwargs.get('cat_slug',None)
        if slug is not None:
            cat=Category.objects.get(slug=slug)
            books=BookModel.objects.filter(category=cat)
        context['books']=books
        context['categorys']=categorys
        return context
    