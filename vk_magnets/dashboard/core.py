#!venv/bin/python
import requests
from PIL import Image
import svgwrite
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

def save_sheet(sheet,index,user_id):
    f1 = open('sheets/{user_id}_{sheet_index}.pdf'.format(user_id=user_id,sheet_index=index),'w')
    sheet.save(f1,"PDF")

def save_album_by_id(user_id):
    friends = get_user_friends(user_id)
    save_album(friends)

def save_album(friends=[],user_id=1):
    sheet_index=1
    sheets = []
    small_pic = []
    sheet = Image.new('RGB',(2480,3508),(255, 255, 255))
    sheet_index = 0
    dwg = svgwrite.Drawing(filename='sheets/{user_id}_{sheet_index}.svg'.format(user_id=user_id,sheet_index=sheet_index),size=(2480,3508))
    shapes = dwg.add(dwg.g(id='shapes',fill='white'))
    pointer = (0,0)
    for friend in friends:
        try:
            response = requests.get(friend[photo_format])
        except KeyError:
            response = requests.get(friend['photo_max_orig'])
        new_image = Image.open(StringIO(response.content))
        #new_image = Image.open('pictures_400x400/{filename}'.format(filename=))
        w, h = new_image.size
        #resizing part. new_image must be 400x400
        if w==400 and h>400:
            new_image = new_image.crop((0,0,400,400))
        if new_image.size == (400,400):
            if pointer[1] > 6:
                if pointer[0] > 3:
                    save_sheet(sheet=sheet,index=sheet_index,user_id=user_id)
                    dwg.save()
                    sheet_index += 1
                    sheet = Image.new('RGB',(2480,3508),(255, 255, 255))
                    dwg = svgwrite.Drawing(filename='sheets/{user_id}_{sheet_index}.svg'.format(user_id=user_id,sheet_index=sheet_index),size=(2480,3508))
                    shapes = dwg.add(dwg.g(id='shapes',fill='white'))
                    pointer = (0,0)
                    box = (90+pointer[0]*460+30,144+pointer[1]*460+30,90+pointer[0]*460+430,144+pointer[1]*460+430)
                    sheet.paste(new_image,box)
                    shapes.add(dwg.rect(insert=(90+pointer[0]*460+30,144+pointer[1]*460+30), size=(400, 400), stroke='red', stroke_width=1))
                    pointer = (0,1)
                else:
                    pointer = (pointer[0]+1,0)
                    box = (90+pointer[0]*460+30,144+pointer[1]*460+30,90+pointer[0]*460+430,144+pointer[1]*460+430)
                    shapes.add(dwg.rect(insert=(90+pointer[0]*460+30,144+pointer[1]*460+30), size=(400, 400), stroke='red', stroke_width=1))
                    sheet.paste(new_image,box)
                    pointer = (pointer[0],1)
            else:
                box = (90+pointer[0]*460+30,144+pointer[1]*460+30,90+pointer[0]*460+430,144+pointer[1]*460+430)
                shapes.add(dwg.rect(insert=(90+pointer[0]*460+30,144+pointer[1]*460+30), size=(400, 400), stroke='red', stroke_width=1))
                sheet.paste(new_image,box)
                pointer = (pointer[0],pointer[1]+1)
        elif w<400:
            small_pic.append(new_image)
    # save_sheet(sheet=sheet,index=sheet_index,user_id=user_id)
    # dwg.save()
    # sheet_index+=1
    if small_pic:
        # dwg = svgwrite.Drawing(filename='sheets/{user_id}_{sheet_index}.svg'.format(user_id=user_id,sheet_index=sheet_index),size=(2480,3508))
        # shapes = dwg.add(dwg.g(id='shapes',fill='white'))
        # sheet = Image.new('RGB',(2480,3508),(255, 255, 255))
        pointer = (90+pointer[0]*460+30,144+pointer[1]*460+30)
        rw = 400
        for image in sorted(small_pic, key=lambda image: image.size[0], reverse=True):
            w,h = image.size
            # if pointer[1]==174:
            #     rw = w #rh - row_height
            if pointer[1]+h > 3400:
                if pointer[0]+rw+w> 2390:
                    save_sheet(sheet=sheet,index=sheet_index,user_id=user_id)
                    dwg.save()
                    sheet_index+=1
                    dwg = svgwrite.Drawing(filename='sheets/{user_id}_{sheet_index}.svg'.format(user_id=user_id,sheet_index=sheet_index),size=(2480,3508))
                    shapes = dwg.add(dwg.g(id='shapes',fill='white'))
                    pointer = (120,174)
                    sheet = Image.new('RGB',(2480,3508),(255, 255, 255))
                    sheet.paste(image,(pointer[0],pointer[1],pointer[0]+w,pointer[1]+h))
                    shapes.add(dwg.rect(insert=pointer, size=(w,h), stroke='red', stroke_width=1))
                    pointer = (pointer[0],pointer[1]+60+h)
                else:
                    pointer = (pointer[0]+60+rw,174)
                    rw = w
                    sheet.paste(image,(pointer[0],pointer[1],pointer[0]+w,pointer[1]+h))
                    shapes.add(dwg.rect(insert=pointer, size=(w,h), stroke='red', stroke_width=1))
                    pointer = (pointer[0],pointer[1]+60+h)
            else:
                sheet.paste(image,(pointer[0],pointer[1],pointer[0]+w,pointer[1]+h))
                shapes.add(dwg.rect(insert=pointer, size=(w,h), stroke='red', stroke_width=1))
                pointer = (pointer[0],pointer[1]+60+h)
        save_sheet(sheet=sheet,index=sheet_index,user_id=user_id)
        dwg.save()
        return "ok"

#save_album_by_id(7284083) #srsatt
#save_album_by_id(1648387) #evgenity
#get_user_friends(1648387)7284083
