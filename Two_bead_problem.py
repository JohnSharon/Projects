
'''Two bead problem'''

import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

############## Used functions ##############

def model(theta,g):
    a=theta[3]; x=theta[1]
    x_1=theta[2]; a_1=theta[4]
    x_2=-g
    dtheta_dt=np.array([1,x_1,x_2,a_1,0])
    return dtheta_dt

def odeint(model,theta,g,h):
   r1=model(theta,g)
   r2=model(theta+(h/2)*r1,g)
   r3=model(theta+(h/2)*r2,g)
   r4=model(theta+(h/2)*r3,g)
   next=np.array(theta+(h/6)*(r1 + 2*r2 + 2*r3 + r4))
   return next

def anglechange_floor(a,b): #changes a to the
                            #nearest arcsin(b)
   a=a%(2*np.pi)
   if(0<a<=(np.pi)/2):
          a=np.arcsin(b)
   if((np.pi)/2<a<=np.pi):
          a=np.pi-np.arcsin(b)
   if((np.pi)<a<=(np.pi)*(3/2)):
          a=np.pi-np.arcsin(b)
   else:
          a=np.arcsin(b)
   return a


#############################

 ####### the solver #################333
def solve(model,theta_0,g,m1,m2,l1,l2):
  
   h=(t2-t1)/N
   arr=np.array([theta_0])

   for i in range(0,500,1):
      
      prev=arr[i,:]
      a=prev[3]; x=prev[1]; a_1=prev[4]; x_1=prev[2]
      c=-l1*np.sin(a)+x

      #when m2 touches the floor break
      if((x+l2*np.sin(a))<0): 
          break                    
      
      #when m1 is in the air
      if (c>0): 
               next=odeint(model,prev,g,h)
        
      #when m2 is on the floor
      if (c<=0):

              #if m2 gets below floor, bring it up
              if(c<0): 
                  a=anglechange_floor(a,x/l1)
        
              #if m2 hits the floor with a velocity toward it
              if((-l1*a_1*np.cos(a)+x_1)<0):
                  v=x_1
                  x_1=(m1*(-v+a_1*l1*(np.cos(a)))+m2*(v+a_1*l2*(np.cos(a))))/(m1+m2)
                  a_1=-(abs((((((np.cos(a)*(3*m1+m2)*l1*a_1)-2*m1*x_1)/(m1+m2))**2)+((np.sin(a)*a_1*l1)**2))**0.5))
              #end of updating x,x_1,a,a_1 due to m1 hitting floor

              arr[i,3]=a
              arr[i,4]=a_1
              arr[i,2]=x_1
              prev=arr[i,:]
              c=-l1*np.sin(a)+x

        #when m1 has more upward force 
              if (((a_1**2)*l1*np.sin(a))>=g):
                  #same as c>0 case
                   next=odeint(model,prev,g,h)
      
        #when m1 has more downward force
              if(((a_1**2)*l1*np.sin(a))<g):

                   g1=(m2*g/(m1+m2))
                   next=odeint(model,prev,g1,h)
                  #update x wrt normal free fall
                  #but then update angle such that
                  #m1 slides along the floor
                   x=next[1]; x_1=next[2]            
                   a=anglechange_floor(a,x/l1)
                   a_1= x_1/((l1**2-x**2)**0.5)            
                   next[3]=a;next[4]=a_1

      arr=np.append(arr,[next],axis=0)

   return arr

#########end of def odeint############

l1=1;l2=1;l=1
g=10
m1=1;m2=1


#initial condition
ang=0
pos=5
avel=6
vel=(m2*l2*avel)/(m1+m2)
theta_0=np.array([0,pos,vel,ang,avel])

#Time points
N=500
t1=0
t2=2


theta1=solve(model,theta_0,g,m1,m2,l1,l2)


x=np.array(theta1[:,1])
a=np.array(theta1[:,3])

x1=-l1*np.cos(a)
y1=x-l1*np.sin(a)
x2=l2*np.cos(a)
y2=x+l2*np.sin(a)

fig= plt.figure()


ax=plt.axes(xlim =(-5, 5), ylim =(0, 10))

circle1 = plt.Circle((x1[0], y1[0]), radius=0.09)
circle2 = plt.Circle((x2[0], y2[0]), radius=0.09)
line, = ax.plot([x1[0], x2[0]],[y1[0], y2[0]], color='k')

ax.add_patch(circle1)
ax.add_patch(circle2)

def update(num, x1, y1,x2,y2, circle1, circle2, line):
    line.set_data([x1[num],x2[num]], [y1[num],y2[num]])
    circle1.center = (x1[num], y1[num])
    circle2.center = (x2[num], y2[num])
    return circle1,circle2,line

ani = animation.FuncAnimation(fig, update, len(x), fargs=[x1,y1,x2,y2,circle1,circle2,line], interval=3, blit=True)

plt.show()
