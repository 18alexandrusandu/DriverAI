import math
import os
import random
import time

import numpy as np
from PIL import Image, ImageDraw, ImageTk
import keyboard
import tkinter
from  keras import models

def distance(x1,y1,x2,y2):
    return math.sqrt( (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def distance_signed(x1,y1,x2,y2):
    return  ((x1-x2)+(y1-y2))/2



def rotatedPhotoImage(img, angle,car):
    angleInRads = -angle * math.pi / 180
    diagonal = math.sqrt(img.width ** 2 + img.height ** 2)
    xmidpoint = img.width/2
    ymidpoint = img.height/2
    newPhotoImage = tkinter.PhotoImage(width=int(diagonal), height=int(diagonal))
    for x in range(img.width):
        for y in range(img.height):

            # convert to ordinary mathematical coordinates
            xnew = float(x)
            ynew = float(-y)

            # shift to origin
            xnew = xnew - xmidpoint
            ynew = ynew + ymidpoint

            # new rotated variables, rotated around origin (0,0) using simoultaneous assigment
            xnew, ynew = xnew*math.cos(angleInRads) - ynew*math.sin(angleInRads), xnew * math.sin(angleInRads) + ynew*math.cos(angleInRads)

            # shift back to quadrant iv (x,-y), but centered in bigger box
            xnew = xnew + diagonal/2
            ynew = ynew - diagonal/2

            # convert to -y coordinates
            xnew = xnew
            ynew = -ynew

            # get pixel data from the pixel being rotated in hex format
            rgb = '#%02x%02x%02x' % img.getpixel((x, y))

            # put that pixel data into the new image
            newPhotoImage.put(rgb, (int(xnew), int(ynew)))

            # this helps fill in empty pixels due to rounding issues
            newPhotoImage.put(rgb, (int(xnew+1), int(ynew)))
    car.image=newPhotoImage
    return newPhotoImage
def sign(x):
    if x>=0:
       return 1
    else:
      return -1

class Car:
    def __init__(self,x,y,v=0,a=0,dir=0,step=10,max_v=400):
        self.x=x
        self.y=y
        self.starty=y
        self.v=v
        self.a=a
        self.max_v=max_v
        self.step=step
        self.color=(255,0,0,255)
        self.width=50
        self.height=100
        self.dir=dir
        self.pointsCar=[]
        self.image="kk;"
        self.controls=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        self.sensor_eq=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    def accelerate(self,rate_t=5):
         self.a=self.a+rate_t


    def frana(self,rate_t=10):
        self.a=self.a-rate_t


    def vireaza_dreapta(self,rate_t=10):
          self.dir=self.dir+rate_t

    def vireaza_stanga(self,rate_t=10):
        self.dir = self.dir -  rate_t

    def update_controls(self):
        x=self.x
        y=self.y
        x1 = self.x - self.width / 2
        x2 = self.x + self.width / 2
        y1 = self.y - self.height / 2
        y2 = self.y + self.height / 2
        xc = (x2 + x1) / 2
        yc = (y2 + y1) / 2
        self.controls[0][0] = math.cos(math.radians(self.dir)) * (x1 - xc) - math.sin(math.radians(self.dir)) * (y1 - yc) + xc
        self.controls[1][0]  = math.cos(math.radians(self.dir)) * (x2 - xc) - math.sin(math.radians(self.dir)) * (y1 - yc) + xc
        self.controls[2][0]  = math.cos(math.radians(self.dir)) * (x2 - xc) - math.sin(math.radians(self.dir)) * (y2 - yc) + xc
        self.controls[3][0] = math.cos(math.radians(self.dir)) * (x1 - xc) - math.sin(math.radians(self.dir)) * (y2 - yc) + xc
        self.controls[0][1]= math.sin(math.radians(self.dir)) * (x1 - xc) + math.cos(math.radians(self.dir)) * (y1 - yc) + yc
        self.controls[1][1] = math.sin(math.radians(self.dir)) * (x2 - xc) + math.cos(math.radians(self.dir)) * (y1 - yc) + yc
        self.controls[2][1] = math.sin(math.radians(self.dir)) * (x2 - xc) + math.cos(math.radians(self.dir)) * (y2 - yc) + yc
        self.controls[3][1] = math.sin(math.radians(self.dir)) * (x1 - xc) + math.cos(math.radians(self.dir)) * (y2 - yc) + yc

        self.controls[4][0] = math.cos(math.radians(self.dir)) * (x - xc) - math.sin(math.radians(self.dir)) * (y1 - yc) + xc
        self.controls[5][0] = math.cos(math.radians(self.dir)) * (x1 - xc) - math.sin(math.radians(self.dir)) * (y - yc) + xc
        self.controls[6][0] = math.cos(math.radians(self.dir)) * (x2 - xc) - math.sin(math.radians(self.dir)) * (y - yc) + xc
        self.controls[7][0] = math.cos(math.radians(self.dir)) * (x - xc) - math.sin(math.radians(self.dir)) * (y2 - yc) + xc
        self.controls[4][1] = math.sin(math.radians(self.dir)) * (x - xc) + math.cos(math.radians(self.dir)) * (y1 - yc) + yc
        self.controls[5][1] = math.sin(math.radians(self.dir)) * (x1 - xc) + math.cos(math.radians(self.dir)) * (y - yc) + yc
        self.controls[6][1] = math.sin(math.radians(self.dir)) * (x2 - xc) + math.cos(math.radians(self.dir)) * (y - yc) + yc
        self.controls[7][1] = math.sin(math.radians(self.dir)) * (x - xc) + math.cos(math.radians(self.dir)) * (y2 - yc) + yc


        for i in range(8):
            self.sensor_eq[i][0]=self.x
            self.sensor_eq[i][1] = self.y
            self.sensor_eq[i][2] =self.controls[i][0]-self.x
            self.sensor_eq[i][3]=self.controls[i][1]-self.y



    def update(self):

        if self.v+self.a <= 0:
            self.a = 0

        if self.v <=0:
            self.v=0

        if self.v >self.max_v:
             self.v=self.max_v
        if self.y<0:
            self.y=self.starty

        self.v=self.v+self.a
        self.x=self.x+self.v*math.sin(math.radians(self.dir))
        self.y = self.y - self.v * math.cos(math.radians(self.dir))
        self.update_controls()





    def do_action(self,action="none",rate_t=5):
        if action=="forward":
            self.accelerate(1)
        if action =="stop":
            self.frana(5)
        if action =="left":
            self.vireaza_stanga(10)
        if action == "right":
          self.vireaza_dreapta(10)
        self.update()

    def collision(self,road):
        b1=road.check_inside(self.x,self.y)
        b2 = road.check_inside(self.controls[0][0], self.controls[0][1])
        b3 = road.check_inside(self.controls[1][0], self.controls[1][1])
        b4=  road.check_inside(self.controls[2][0], self.controls[2][1])
        b5 = road.check_inside(self.controls[3][0], self.controls[3][1])
        b6=road.check_inside((self.controls[0][0]+self.controls[3][0])/2, (self.controls[0][1]+self.controls[3][1])/2)
        b7=road.check_inside((self.controls[0][0]+self.controls[3][0])/2, (self.controls[0][1]+self.controls[3][1])/2)
        b8=road.check_inside((self.controls[0][0]+self.controls[3][0])/2, (self.controls[0][1]+self.controls[3][1])/2)
        b9=road.check_inside((self.controls[0][0]+self.controls[3][0])/2, (self.controls[0][1]+self.controls[3][1])/2)
        return b2 or b1 or b3 or b4 or b5 or b6 or b7 or b8 or b9
    def sensors_data(self,road,can):
        s=[0,0,0,0,0,0,0,0,0]
        for i in range(8):
         s[i]=road.minim_distance_eq(self.sensor_eq[i][0],self.sensor_eq[i][1],self.sensor_eq[i][2],self.sensor_eq[i][3])

         if s[i][0]<=-10000 and (i==1 or i==2 or i==6):
             s[i][0]=10000
         can.create_oval(s[i][1][0],s[i][1][1],s[i][1][0]+10,s[i][1][1]+10,fill="#ff0000")

        i=0
        for c in self.controls:
          can.create_oval(c[0], c[1],c[0]+10, c[1]+10, fill="#476042")
          can.create_line(int(c[0]),int(c[1]),int(s[i][1][0]),int(s[i][1][1]),fill="#00ffff")
          i+=1

        sensors=[s[0][0],s[1][0],s[2][0],s[3][0],s[4][0],s[5][0],s[6][0],s[7][0]]
        return sensors



    def drawCar(self,img):
        draw =ImageDraw.Draw(img)
        draw.polygon([(self.controls[0][0],self.controls[0][1]),
                      (self.controls[1][0],self.controls[1][1]),
                      (self.controls[2][0],self.controls[2][1]),
                      (self.controls[3][0],self.controls[3][1])], fill=self.color)

    def drawCarCanvas(self,can):
        img=Image.open("images/red_car.jpg")
        img.resize((self.width,self.height))
        rotatedPhotoImage(img,self.dir,self)

        can.create_image(self.x,self.y,image=self.image, anchor="center")








class Road:
    def __init__(self,center_road,points_left=[],points_right=[]):
        self.points_left=points_left
        self.points_right=points_right
        self.color=(0,0,0)
        self.width_Road=125
        self.center_road=center_road
    def add_point_left(self,point):
        self.points_left.append(point)
    def add_point_right(self,point):
        self.points_right.append(point)


    def minim_distance(self,x,y):
        dist=distance_signed(x, y, self.points_right[0][0], self.points_right[0][1])
        for p in range(len(self.points_right) - 1):
            distp=distance_signed(x, y, self.points_right[p][0], self.points_right[p][1])
            if  abs(distp) < abs(dist):
                dist=distp

        for p in range(len(self.points_left) - 1):

            distp =distance_signed(x, y, self.points_left[p][0], self.points_left[p][1])
            if abs(distp) < abs(dist):
               dist = distp

        return dist
    def minim_distance_eq(self,x1,y1,dx,dy):
        print(x1,y1,dx,dy)
        min_dist=-10000
        cent_dist=10000
        min_p=[0,0]
        scale=0
        for p in self.points_right+self.points_left:
            count=0
            scale=0
            avgd=0
            if not dx==0:
              tx=(p[0]-x1)/dx
              if tx>0:
                count+=1
                scale+=1
                avgd+=tx*tx
            else:
              count+=1

            if not dy==0:
              ty=(p[1]-y1)/dy
              if ty>=1:
                  count += 1
                  scale+=1
                  avgd += ty*ty
            else:
                count +=1

            if count==2:
                cent_distp = distance(x1, y1, p[0], p[1])
                avgd=math.sqrt(avgd)
                if min_dist==-10000:
                    min_dist=avgd
                    min_p = [p[0],p[1]]
                    cent_dist = cent_distp
                else:
                    if avgd<=min_dist and cent_distp<cent_dist:
                        min_dist=avgd
                        min_p = [p[0], p[1]]
                        cent_dist=cent_distp
        return [min_dist,min_p]

    def check_inside(self,x,y):


         for p in range(len(self.points_right)-1):
          if distance(x,y,self.points_right[p][0],self.points_right[p][1])<self.width_Road/10:

                return True

         for p in range(len(self.points_left) - 1):
             if distance(x, y, self.points_left[p][0], self.points_left[p][1]) <self.width_Road/10:
                 return True


         return False

    def generate_road(self,start_y=400,dist=20):
      point_of_reference_y=start_y
      point_of_reference_x=self.center_road[0]-self.width_Road

      while start_y >0:
       start_y=start_y-dist
       var_side=random.random()*2
       dir_var=sign(1-var_side)
       n1x=point_of_reference_x + dir_var*(0.5+random.random()*10)
       n1y=start_y
       n2x= n1x+self.width_Road
       n2y=start_y
       self.add_point_left([n1x,n1y])
       self.add_point_right([n2x,n2y])
       point_of_reference_x=n1x

    def generate_point_road(self,y,dist=20):
        var_side = random.random() * 2
        dir_var = sign(1 - var_side)
        por=self.points_left[len(self.points_left)-1][0]
        if por >800:
            por=800-self.width_Road/2
        if por<=0:
            por = 10

        n1x = por + dir_var * (0.5+random.random() * 10)
        n1y = y
        n2x = n1x + self.width_Road
        n2y = y
        self.add_point_left([n1x, n1y])
        self.add_point_right([n2x, n2y])

    def shift_points(self,size):
       for p in self.points_left:
           p[1]+=size
           p[1]=max(0,p[1])
       for p in self.points_right:
           p[1] += size
           p[1] = max(0, p[1])

    def delete_redundant(self,height):
        right=[]
        for p in self.points_right:
            if p[1]<height:
                right.append(p)
        self.points_right=right
        left=[]
        for p in self.points_left:
            if p[1]<height:
                left.append(p)
        self.points_left = left


    def draw_road_boundary(self,img):
        draw = ImageDraw.Draw(img)
        left=[]
        right=[]
        for p in self.points_right:
            right.append((p[0],p[1]))
        for p in self.points_left:
            left.append((p[0], p[1]))

        draw.line(left, width=5, fill=self.color, joint="curve")
        draw.line(right, width=5, fill=self.color, joint="curve")
    def draw_road_canvas(self,can):
        list1=[]
        list2=[]
        for p in self.points_left:
          if p[0]>0 and p[1]>0:
            list1.append(p[0])
            list1.append(p[1])
        for p in self.points_right:
         if p[0] > 0 and p[1] > 0:
            list2.append(p[0])
            list2.append(p[1])

        can.create_line(list1, width=5, fill="black")
        can.create_line(list2, width=5, fill="black")



def draw_world(car,road,img,name_img="world.png"):
     car.drawCar(img)
     road.draw_road_boundary(img)
     img.save(name_img)



def draw_Canvas(car, road,can, name_img="world.png"):
    road.draw_road_canvas(can)
    car.drawCarCanvas(can)


def useModel():
     model=models.load_model("model")
     return model
def simulate():
    model=0
    f=0
    width=800
    height=800
    window = tkinter.Tk()
    window.title('Hello Python')
    window.geometry(str(height)+"x"+str(width)+"+10+20")
    can = tkinter.Canvas(window)
    can.configure(bg="#9F9393")
    can.pack(fill="both", expand=True)
    nr_img=0
    automated=False
    car=Car(width/2,height-100)
    road=Road((width/2+100,car.y))
    road.generate_road(height)
    stop=False
    history_saved=False
    relearn=False
    val=os.system('del "C:/Users/Alexandru Andercou/Desktop/SRF_proiect_DRIVER_AI/pythonProject/images/.*"')
    print("val",val)

    while not stop:

     draw_Canvas(car, road, can)
     if history_saved:
         sensors = car.sensors_data(road, can)
         print("save sensed", sensors)

     if keyboard.is_pressed("h") and history_saved==False:
         f = open("data_AI_DRive.csv", "w")
         sensors = car.sensors_data(road, can)
         history_saved=True



     print("here we go again")
     pressed=False
     if keyboard.is_pressed("s"):
          stop=True
          break
     if keyboard.is_pressed("a"):
         model=useModel()
         automated = True
         print("on automated mode")

     if automated:
         sensors = car.sensors_data(road, can)
         if keyboard.is_pressed("r"):
             print("relearn")
             history_saved=False
             f=open("data_AI_DRive.csv","a")
             relearn=True

     window.update()
     time.sleep(0.2)
     can.delete("all")
     if automated :
        print("on automated mode")
        prd=model.predict(np.array(sensors+[car.v,car.dir]).reshape(1, -1))
        prd=prd[0]




        index=next(i for i, x in
                   enumerate(prd) if x == max(prd))
        print("prediction:", prd,index)
        if index==0 and not relearn:
            #car.do_action("forward")
            pass
        if index == 1 and not relearn:
             car.do_action("stop")
        if index == 2 and not relearn:
            car.do_action("left")
        if index== 3 and not relearn:
            car.do_action("right")
     if relearn and automated:
         autopress=False
         if keyboard.is_pressed("up"):
           f.write("forward\n")
           autopress = True
         else:
          if keyboard.is_pressed("down"):
             f.write("stop\n")
             autopress = True
          else:
           if keyboard.is_pressed("right"):
             f.write("right\n")
             autopress = True
           else:
            if keyboard.is_pressed("left"):
             f.write("left\n")
             autopress = True


         if autopress==False:
             f.write("forward\n")

         for s in sensors:
           f.write(str(s) + " ")
         f.write(str(car.v ) + " ")
         f.write(str(car.dir) + " ")
         f.write("\n")


     if keyboard.is_pressed("up"):
       if history_saved:
        nr_img += 1
        img = Image.new('RGB', (width, height), color='gray')
        draw_world(car, road, img,"images/images/go_forward_"+str(nr_img)+".jpg")
        f.write("forward\n")
        for s in sensors:
           f.write(str(s)+" ")
        f.write(str(car.v)+" ")
        f.write(str(car.dir) + " ")
        f.write("\n")
       car.do_action("forward")
       pressed=True
     if keyboard.is_pressed("down"):
       if history_saved:
        img = Image.new('RGB', (width, height), color='gray')
        nr_img += 1
        draw_world(car, road, img,"images/images/go_stop_"+str(nr_img)+".jpg")
        f.write("stop\n")
        for s in sensors:
          f.write(str(s)+" ")
        f.write(str(car.v)+" ")
        f.write(str(car.dir) + " ")
        f.write("\n")

       car.do_action("stop")
       pressed=True
     if keyboard.is_pressed("left"):
       if history_saved:
        img = Image.new('RGB', (width, height), color='gray')
        nr_img += 1
        draw_world(car, road, img, "images/images/go_left_" + str(nr_img)+".jpg")
        f.write("left\n")
        for s in sensors:
          f.write(str(s) + " ")
        f.write(str(car.v)+" ")
        f.write(str(car.dir) + " ")
        f.write("\n")
       car.do_action("left")
       pressed=True
     if keyboard.is_pressed("right"):
        if history_saved:
         f.write("right\n")
         for s in sensors:
             f.write(str(s) + " ")
         f.write(str(car.v) + " ")
         f.write(str(car.dir)+ " ")
         f.write("\n")
         img = Image.new('RGB', (width, height), color='gray')
         nr_img += 1
         draw_world(car, road, img, "images/images/go_right_" + str(nr_img)+".jpg")
        car.do_action("right")
        pressed = True
     if not pressed:
      if history_saved:
             f.write("forward\n")
             for s in sensors:
                 f.write(str(s) + " ")
             f.write(str(car.v ) + " ")
             f.write(str(car.dir) + " ")
             f.write("\n")
      car.update()

     car.y = height - 150
     car.update_controls()
     if car.collision(road)==True:
          #stop=True
          can.create_text(width/2,height/2,text="YOU LOST",fill="black",font=('Helvetica 35 bold'))

     road.shift_points(car.v)

     for r in range(0,car.v):
         if r % 20 == 0:
             road.generate_point_road(-r)
     road.delete_redundant(height)

     print("not stuck")



     print("not struck")

    f.close()
