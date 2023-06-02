from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from whois import whois 
from dns.resolver import resolve


# Create your views here.
def index(request):
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
        if 'MX' in mx:
            for i in range(0, len(mx), 3):
                formatted_mx += f"Type: {mx[i]}\nPriority: {mx[i+1]}\nValue: {mx[i+2]}\n\n"
        else:
            for i in range(0, len(mx), 2):
                formatted_mx += f"Type: MX\nPriority: {mx[i]}\nValue: {mx[i+1]}\n\n"
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
        
@csrf_exempt
def domain(request):
    template = loader.get_template("tools/domain.html")
    whois_data = 0
    domain = 0
    if request.method == "POST":
        domain = str(request.POST["domain"]).replace('https://', '').replace('http://', '').replace('/','')
        #Gathering and formatting WHOIS data
        try: 
            whois_data = whois(domain)
        except Exception as e:
            print(e)
            context = {
                "no_domain" : 1,
                "e" : e,
            }
            return HttpResponse(template.render(context, request))
        
        if(whois_data["domain_name"]) == None:
            context = {
                "no_domain" : 1,
            }
            return HttpResponse(template.render(context, request))
        
        if type(whois_data["domain_name"]) == list:
            domain_name = whois_data["domain_name"][0].lower()
        else:
            domain_name = whois_data["domain_name"].lower()
        registrar = whois_data["registrar"]

        if type(whois_data["updated_date"]) == list:
            updated_date = whois_data["updated_date"][0]
        else:
            updated_date = whois_data["updated_date"]

        if type(whois_data["creation_date"]) == list:
            creation_date = whois_data["creation_date"][0]
        else:
            creation_date = whois_data["creation_date"]

        if type(whois_data["expiration_date"]) == list:
            expiration_date = whois_data["expiration_date"][0]
        else:
            expiration_date = whois_data["expiration_date"]
        if type(whois_data["name_servers"]) == list:
            for i in range(0, len(whois_data["name_servers"])):
                whois_data["name_servers"][i] = whois_data["name_servers"][i].lower()
            name_servers = set(whois_data["name_servers"])
        else:
            whois_data["name_servers"] = whois_data["name_servers"].lower()
            name_servers = whois_data["name_servers"]
        
        status = whois_data["status"]

        #Gathering and formatting DNS records
        try:
            blank_a = resolve(domain, 'A')
        except Exception as e:
            print(e)
            blank_a = "None"
        try:
            www_a = resolve(f'www.{domain}', 'A')
        except Exception as e:
            print(e)
            www_a = "None"
        try:
            mx = resolve(domain, "MX")
        except Exception as e:
            print(e)
            mx = "None"
        try:
            ns = resolve(domain, "NS")
        except Exception as e:
            print(e)
            ns = "None"
        try:
            txt = resolve(domain, "TXT")
        except Exception as e:
            print(e)
            txt = "None"
    if whois_data == 0:
        context = {

        }
    else:
        context = {
            "domain_name" : domain_name,
            "registrar" : registrar,
            "updated_date" : updated_date,
            "creation_date" : creation_date,
            "expiration_date" : expiration_date,
            "name_servers" : name_servers,
            "status" : status,
            "blank_a" : blank_a,
            "www_a" : www_a,
            "mx" : mx,
            "ns" : ns,
            "txt" : txt,
            }
    return HttpResponse(template.render(context, request))
