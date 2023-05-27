import json
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def privacy_policy(request):
    
    f = open('privacy-policy.json')
    
    data = json.load(f)
    return JsonResponse(data)

def edit_privacy_policy(request):
   try: 
        request_data = json.loads(request.body)    
        
        with open('privacy-policy.json', 'r+') as f:
                data = json.load(f)
                data['privacy-policy'] = request_data['privacy-policy']# <--- add `id` value.
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part
                
        messages.success(request, 'Privacy Policy updated successfully.')       
        return JsonResponse({"success": True, "data": data})
   except:
        return JsonResponse({"success": False, "error": "Something went wrong."})

