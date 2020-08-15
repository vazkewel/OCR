import cv2
import pytesseract
import numpy as np
from wand.image import Image as wi

output = open("output.txt","w")  #final output is stored in this file


pdf1 = wi(filename="C:\Users\kewel\Desktop\Projects\empezar\ocr\OCR\PDFs\OCR_1.pdf", resolution=200) #enter pdf location here OCR_1
pdf2 = wi(filename="C:\Users\kewel\Desktop\Projects\empezar\ocr\OCR\PDFs\OCR_2.pdf", resolution=200) #enter pdf location here OCR_2
pdfimage1 = pdf1.convert("png")
pdfimage2 = pdf2.convert("png")
i=1
for img in pdfimage1.sequence:
    page = wi(image=img)
    page.save(filename="OCR_1.png")
    i +=1
filename1 = "OCR_1.png"

for img in pdfimage2.sequence:
    page = wi(image=img)
    page.save(filename="OCR_2.png")
    i +=1
    
filename2 = "OCR_2.png"


def verify(x):
    g = "bcdefghijk"
    g1="lmnopqrstu"
    g2="vwxyz"
    ds = {}
    k= 12
    ds['a']=10
    for i in g:
        ds[i]=k
        k+=1
    k+=1
    for i in g1:
        ds[i]=k
        k+=1
    k+=1
    for i in g2:
        ds[i]=k
        k+=1    
    main_ch = x[:-1]
    check = int(x[-1:])
    print main_ch,check
    first_no=0
    ast_no=0
    l=0
    for i in main_ch:
        if i.lower() in ds:first_no+=ds[i.lower()]*2**l
        else:first_no+=int(i)*2**l
        l+=1
    print first_no
    last_no=first_no - (first_no/11)*11 
    if last_no==int(check):return "CTR no. correct"
    else:return "CTR no. incorrect"







##img = cv2.imread(filename1)
##image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
##ac_height = img.shape[0]
##ac_width = img.shape[1]
##blur = cv2.GaussianBlur(image,(5,5),0)
##j=False
##p=True
##ret,thresh1 = cv2.threshold(blur,232,255,cv2.THRESH_BINARY)
##
##keywords = ["IEC","Port of Loading", "Port of Discharge", "Gross Wt", "Country of Dest", "Total Pkgs","Loose pckts", "Net Wt","No.of Ctrs"]
##
##thresh2 = thresh1.copy()
##repeat = []
##output.write("OCR_1 output:\n")
##for n in range(0,ac_height,100):
##    for m in [500,ac_width]:
##        if m == ac_width: y=500
##        else:y=0
##        x=n
##        h=m
##        w=x+300
##        crop_image = thresh1[x:w, y:h]
##        text = pytesseract.image_to_string(crop_image)
##        keywords = [i for i in keywords if i not in repeat]
##        for i in keywords:
##            if i in text:
##                data = pytesseract.image_to_data(crop_image, output_type=pytesseract.Output.DICT)
##                res = i.split()
##                word_occurences = [ k for k, word in enumerate(data["text"]) if word == res[0] ]
##                d_list = data['text']
##                for o in range(len(d_list)):
##                    if d_list[o] == res[0]:
##                        for u in range(len(res)):
##                            if res[u] in d_list[o+u]:j=True
##                            else:j= False  
##                        if j == True:
##                            occ = o
##                            break
##                width = data["width"][occ]
##                height = data["height"][occ]
##                left = data["left"][occ]
##                top = data["top"][occ]
##                blur2 = cv2.GaussianBlur(image,(5,5),0)
##                contrast = [210,238,140,226]
##                for t in contrast:
##                    ret1,thresh2 = cv2.threshold(blur2,t,255,cv2.THRESH_BINARY)
##                    if m==500:crop_im = thresh2[x+top-5:x+top+35, left:710]
##                    else:crop_im = thresh2[x+top-5:x+top+35, 500+left:1653]
##                    text2 = pytesseract.image_to_string(crop_im)
##                    res.append(":")
##                    for f in res:
##                        if f not in text2:
##                            p = False
##                            break
##                        else:p = True
##                    if p==True:break
##                repeat.append(i)
##                check = list(text2)
##                for i in range(len(check)):
##                    if ord(check[i]) > 128:
##                        if ord(check[i])==169:check[i]="0"
##                        else:check[i]=""
##                text3 = ''.join([str(elem) for elem in check])
##                print text3
##                output.write(text3.splitlines()[0]+"\n")
##                cv2.imwrite("C:\Users\kewel\Downloads\OCR_1 (1)\OCR_1-1_test1.png", crop_im)
##
##                
"""code for 2nd pdf """
output.write("\n")
output.write("OCR_2 output:\n")
img2 = cv2.imread(filename2)
image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
ac_height = img2.shape[0]
ac_width = img2.shape[1]
blur = cv2.GaussianBlur(image2,(1,1),0)
lines=200
j=False
p=True
ret,thresh1 = cv2.threshold(blur,180,255,cv2.THRESH_BINARY)
#keywords = ["CTR No","size","Seal No.","Date"]
#keywords2 = ["CTR No","size","Seal No.","Date"]
keywords = ["CTR No"]
keywords2 = ["CTR No"]
thresh2 = thresh1.copy()
repeat = []

for n in range(0,ac_height,100):
    for m in [500,ac_width]:
        if m == ac_width: y=500
        else:y=0
        x=n
        h=m
        w=x+300
        crop_image = thresh1[x:w, y:h]
        text = pytesseract.image_to_string(crop_image)
        keywords = [i for i in keywords if i not in repeat]
        for i in keywords:
            if i in text:
                data = pytesseract.image_to_data(crop_image, output_type=pytesseract.Output.DICT)
                res = i.split()
                word_occurences = [ k for k, word in enumerate(data["text"]) if word == res[0] ]
                d_list = data['text']
                for o in range(len(d_list)):
                    if d_list[o] == res[0]:
                        for u in range(len(res)):
                            if res[u] in d_list[o+u]:j=True
                            else:j= False 
                        if j == True:
                            occ = o
                            break
                width = data["width"][occ]
                height = data["height"][occ]
                left = data["left"][occ]
                top = data["top"][occ]
                top_next = data["top"][occ+u+1]
                if (top_next - top) <20:left_next = data["left"][occ+u+1]
                else:left_next = left+ 250
                blur2 = cv2.GaussianBlur(image2,(1,1),0)
                ret1,thresh2 = cv2.threshold(blur2,180,255,cv2.THRESH_BINARY)
                if m==500:crop_im = thresh2[x+top-5:x+top+lines, left:left_next+50]
                else:crop_im = thresh2[x+top-5:x+top+lines, 500+left:500+left_next+50]
                cv2.imwrite("C:\Users\kewel\Downloads\OCR_2\OCR_2-1_test211.png", crop_im)
                data2 = pytesseract.image_to_data(crop_im, output_type=pytesseract.Output.DICT)
                wid = 0
                for h in range(len(data2["text"])):
                    if data2["word_num"][h] ==1 and data2["width"][h] > wid and data2["line_num"][h]>0 and any(ch.isalpha() for ch in data2["text"][h]):
                        wid = data2["width"][h]
                        if data2["word_num"][h+1] < data2["word_num"][h]:
                            if data2["width"][h] <100:new_lim = left+300
                            else:new_lim=data2["width"][h]+left
                        else:new_lim=data2["left"][h+1]+left
                if i == "size" :blur3 = cv2.medianBlur(image2,1) 
                else: blur3 = cv2.GaussianBlur(image2,(5,5),0)   
                contrast = [173, 153, 154, 145]
                t = contrast[keywords2.index(i)]
                ret2,thresh3 = cv2.threshold(blur3,t,255,cv2.THRESH_BINARY)
                if m==500:crop_im2 = thresh3[x+top-5:x+top+lines, left:new_lim]
                else:crop_im2 = thresh3[x+top-5:x+top+lines, 500+left:500+new_lim]
                text2 = pytesseract.image_to_string(crop_im2)
                check2 = list(text2)
                for q in range(len(check2)):
                    if ord(check2[q]) > 128:
                        if ord(check2[q])==169:check2[q]="0"
                        else:check2[q]=""
                text3 = ''.join([str(elem) for elem in check2])
                output.write(i+"\n")
                print text3
                if i=="CTR No":
                    for fg in text3.splitlines():
                        if len(fg)==11: print verify(fg)
                
                a=1
                for w in range(1,len(text3.splitlines())):
                    if text3.splitlines()[w] not in [""," ","-"]:
                        output.write(str(a)+")"+text3.splitlines()[w]+"\n")
                        a+=1
                repeat.append(i)

                
output.close()

