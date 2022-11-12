import os

def rename_and_upload(photo, name):
    """"
    A function that will handle profile photo upload
    """
    #read the temporary uploaded file
    with open('media/temp.webp', 'wb+') as destination:
       for chunk in photo.chunks():
            destination.write(chunk)
            
    new_name = destination.name.split('/')
    #the path where to save the photo
    final_path = "%s/photos/%s.webp"%(new_name[0], name)
            
    os.replace(destination.name, final_path)     
    return 'photos/%s.webp'%(name)
  

            