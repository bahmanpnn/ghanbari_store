from django.shortcuts import render
from django.views import View


class AboutUsView(View):
    template_name="about_us_module/about_us.html"
    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        pass