from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    print(request)
    template = loader.get_template("tools/index.html")
    context = { 
        
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def mx_converter(request):
    if request.method == "POST":
        mx = str(request.POST["mx"])
        mx = mx.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("IN", "").strip().split()
        formatted_mx = ""
        for i in range(0, len(mx), 3):
            formatted_mx += f"Type: {mx[i]}\nPriority: {mx[i+1]}\nValue: {mx[i+2]}\n\n"
        mx = formatted_mx
        template = loader.get_template("tools/mx_converter.html")
        context = {
            "mx": mx,
        }
    else:
        template = loader.get_template("tools/mx_converter.html")
        context = {

    }
    
    return HttpResponse(template.render(context, request))