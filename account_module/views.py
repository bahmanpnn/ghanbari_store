from django.shortcuts import render
from django.views import View


class UserRegisterView(View):
    template_name='account_module/register.html'
    
    def get(self,request):
        return render(request,self.template_name)