Program for OCR written in python, to extract the following information from the given shipmnt documents(pdf)

OCR_1.pdf --> Pick values of labels
IEC
Port of Loading
Port of Discharge
Gross wt(KGS)
Country of Dest
Total Pkgs
Loose pckts
Net wt (KGS)
No.of Ctrs

OCR_2.pdf --> Pick table values
CTR No.
Size
Seal No.
Date

Requirements:
1) pip install pytesseract, wand, opencv-python
2)IDLE Python IDE

Procedure:
1)Fetch the pdf files using the wand library
2)Convert the pdf files to image for better processing
3)Use opencv libary to view/edit the image
4)perform a guassian blur on the given image to reduxe the noise, then search through small sections of the at a time to find the required data
5)Once found crop the image arounf the information required
6)Use pytesseract library to convert the cropped image to text

#######################################################################################################################
code

import cv2
import pytesseract
import numpy as np
from wand.image import Image as wi

output = open("output.txt","w")  #final output is stored in this file


pdf1 = wi(filename="C:\Users\kewel\Desktop\ocr\PDFs\OCR_1.pdf", resolution=200) #enter pdf location here OCR_1
pdf2 = wi(filename="C:\Users\kewel\Desktop\ocr\PDFs\OCR_2.pdf", resolution=200) #enter pdf location here OCR_2
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

img = cv2.imread(filename1)
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
ac_height = img.shape[0]
ac_width = img.shape[1]
blur = cv2.GaussianBlur(image,(5,5),0)
j=False
p=True
ret,thresh1 = cv2.threshold(blur,232,255,cv2.THRESH_BINARY)

keywords = ["IEC","Port of Loading", "Port of Discharge", "Gross Wt", "Country of Dest", "Total Pkgs","Loose pckts", "Net Wt","No.of Ctrs"]

thresh2 = thresh1.copy()
repeat = []
output.write("OCR_1 output:\n")
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
                blur2 = cv2.GaussianBlur(image,(5,5),0)
                contrast = [210,238,140,226]
                for t in contrast:
                    ret1,thresh2 = cv2.threshold(blur2,t,255,cv2.THRESH_BINARY)
                    if m==500:crop_im = thresh2[x+top-5:x+top+35, left:710]
                    else:crop_im = thresh2[x+top-5:x+top+35, 500+left:1653]
                    text2 = pytesseract.image_to_string(crop_im)
                    res.append(":")
                    for f in res:
                        if f not in text2:
                            p = False
                            break
                        else:p = True
                    if p==True:break
                repeat.append(i)
                check = list(text2)
                for i in range(len(check)):
                    if ord(check[i]) > 128:
                        if ord(check[i])==169:check[i]="0"
                        else:check[i]=""
                text3 = ''.join([str(elem) for elem in check])
                print text3
                output.write(text3.splitlines()[0]+"\n")
                cv2.imwrite("C:\Users\kewel\Downloads\OCR_1 (1)\OCR_1-1_test1.png", crop_im)

                
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
keywords = ["CTR No","size","Seal No.","Date"]
keywords2 = ["CTR No","size","Seal No.","Date"]
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
                print text2
                check2 = list(text2)
                for q in range(len(check2)):
                    if ord(check2[q]) > 128:
                        if ord(check2[q])==169:check2[q]="0"
                        else:check2[q]=""
                text3 = ''.join([str(elem) for elem in check2])
                output.write(i+"\n")
                a=1
                for w in range(1,len(text3.splitlines())):
                    if text3.splitlines()[w] not in [""," ","-"]:
                        output.write(str(a)+")"+text3.splitlines()[w]+"\n")
                        a+=1
                repeat.append(i)

                   
output.close()


#####################################################################################################################################

OUTPUT

OCR_1 output:
Port of Loading :ICD THAR DRY PORT KA
Port of Discharge:Norfolk
Gross Wt(KGS)  :12320.000
Country of Dest :UNITED STATES
Total Pkgs. : 2800
Loose pckts : 0
No.of Ctrs. : 2
IEC :X
Net Wt(KGS) :10920.000

OCR_2 output:
size
1)40
2)40
Date
1)/20-FEB-20
CTR No
1)TCLU4990548
2)FCIU3982469
Seal No.
1)BOLTO1192950
2)BOLT01192979



