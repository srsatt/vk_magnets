#!venv/bin/python
import requests
from PIL import Image
from StringIO import StringIO
import os
import re
photo_format="photo_400_orig"

def get_user_friends(user_id):
    import requests
    friends = requests.get(url='https://api.vk.com/method/friends.get?user_id=' + str(user_id) +
            '&v=5.25&fields=sex,'+photo_format+",photo_max,photo_max_orig").json()['response']['items']
    good=[]
    for f in friends:
        #try:
        if not re.search(r'(camera|deactivated)',f['photo_max']):
        #if f[photo_format]!='https://vk.com/images/deactivated_400.png' and f[photo_format]!='http://vk.com/images/camera_400.png':
            good.append(f)
            #print f[photo_format]
        #except KeyError:
            pass
    return good


def batch(iterable, n=1):
	    l = len(iterable)
	    for ndx in range(0, l, n):
	        yield iterable[ndx:min(ndx + n, l)]
#temporary
def download_image(url,name):
    f1=open('pictures_max/{name}.png'.format(name=name),'w')
    url = f[photo_format]
    r=requests.get(url)
    print >>f1,r.content
    f1.close()

#A4format @300dpi 2480 Pixels	3508 Pixels
#1mm @300 dpi = 12 px
#margin 2.5*12*2 = 60 px => img 460x460 px
#margin_left=margin_right
#(2480-460*5)/2 = 90
#margin_top
#(3508-460*7)/2=144
#7*5 = 35 friends in sheet

def save_album(user_id):
    friends = get_user_friends(user_id)
    sheet_index=1
    sheets = []
    for sheet_arr in batch(friends,35):
        sheet = Image.new('RGB',(2480,3508),(255, 255, 255))
        for (i,j) in [(i,j) for i in range(5) for j in range(7)]:
            if (i*7+j)<len(sheet_arr):
                try:
                    response = requests.get(sheet_arr[i*7+j][photo_format])
                except KeyError:
                    response = requests.get(sheet_arr[i*7+j]['photo_max_orig'])
                new_image = Image.open(StringIO(response.content))
                #new_image = Image.open('pictures_400x400/{filename}'.format(filename=))
                w, h = new_image.size
                #resizing part. new_image must be 400x400
                if new_image.size!=(400,400):
                    if w==400 and h>400:
                        new_image = new_image.crop((0,0,400,400))
                    elif w<400 and h<400:
                        new_new_image = Image.new('RGB',(400,400),(255, 255, 255))
                        new_new_image.paste(new_image,(0,0,w,h))
                        new_image = new_new_image
                    elif w<400 and h>400:
                        new_image = new_image.crop((0,0,w,400))
                        new_new_image = Image.new('RGB',(400,400),(255, 255, 255))
                        new_new_image.paste(new_image,(0,0,w,400))
                        new_image = new_new_image

                box=(90+i*460+30,144+j*460+30,90+i*460+430,144+j*460+430)
                sheet.paste(new_image,box)
        f1 = open('sheets/{user_id}_{sheet_index}.pdf'.format(user_id=user_id,sheet_index=sheet_index),'w')
        sheet_index+=1
        sheets.append(sheet)
        sheet.save(f1,"PDF")
    f1 = open('sheets/{user_id}.pdf'.format(user_id=user_id),'w')
    #for s in sheets:
    sheets[0].save('sheets/album.pdf',save_all=True, append_images=sheets[1:])
save_album(1648387)
#get_user_friends(1648387)7284083
'''for friend in get_user_friends(1648387):
    try:
        f400 = Image.open(StringIO(requests.get(friend['photo_400_orig']).content))
    except KeyError:
        f400 = '(---, ---)'
    #fmax = Image.open(StringIO(requests.get(friend['photo_max']).content))
    fmax_orig = Image.open(StringIO(requests.get(friend['photo_max_orig']).content))
    try:
        print f400.size, fmax_orig.size
    except AttributeError:
        print f400, fmax_orig.size'''
