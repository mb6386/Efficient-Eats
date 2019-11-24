from django import template

register = template.Library()
@register.filter
def redirect_drinks(url):
    url = url.strip("/")
    breakdown=url.split("/")
    no_drinks_found = False
    new_url=""
    for i in range(len(breakdown)):
        if breakdown[i] == "no-drinks":
            breakdown[i]=""
            no_drinks_found=True

    if no_drinks_found==True:
        for item in breakdown:
            if item != "":
                new_url+=(item+"/")
    else:
        if (len(breakdown)) > 2:
            for i in range(len(breakdown)):
                if i == 2:
                    new_url+="no-drinks/"
                new_url+=(breakdown[i]+"/")
        else:
            new_url=url+'/no-drinks/'
    return new_url
