import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

masa_carro = 2 
masa_pertiga = 1 
longitud_pertiga = 1 


def calcula_aceleracion(tita, v, f):
    numerador = constants.g * np.sin(tita) + np.cos(tita) * ((-f - masa_pertiga * longitud_pertiga * np.power(v, 2) * np.sin(tita)) / (masa_carro + masa_pertiga))
    denominador = longitud_pertiga * (4/3 - (masa_pertiga * np.power(np.cos(tita), 2) / (masa_carro + masa_pertiga)))
    return numerador / denominador

class difuso:
  def __init__(self,dominio):
    self.dominio=dominio
    self.conjunto=list
    self.PF=list

  def difuso_y(self):                                #Se considera un solapamiento de 50% entre los conjuntos
    intervalo=(self.dominio[1]-self.dominio[0])/5    #Se definen 5 intervalos NG(negativo grande),NP(negativo pequenio),Z(zero),PP(positivo pequenio),PG(positivo grande)
    Z=[-intervalo,intervalo]
    PP=[0,2*intervalo]
    PG=[intervalo,self.dominio[1]]
    NP=[-2*intervalo,0]
    NG=[self.dominio[0],-intervalo]
    self.conjunto=[NG,NP,Z,PP,PG]
    return self.conjunto

  def valor_pertenencia(self,x):
    i=0
    pertenencia=[0,0,0,0,0]
    for intr in self.conjunto: #analiza en orden NG,NP,Z,PP,PG para saber en que conjunto esta el numero y les asigna su valor de pertenencia. 
      a=intr[0]                #extremo menor
      c=intr[1]                #extremo mayor
      b=(a+c)/2                #centro
      if x<a:
        pertenencia[i]=0
      if a<=x<=b:
        if i==0:
          pertenencia[0]=1
        else:
          pertenencia[i]=(x-a)/(b-a)
      if b<x<=c:
        if i==4:
          pertenencia[4]=1
        else:
          pertenencia[i]=(x-c)/(b-c)
      if x>c:
        pertenencia[i]=0
      i=i+1    
    return pertenencia

  def tabla(self,ptita,pomega): #Se ingresa el valor de pertenencia de tita y tita' para obtener los valores de pertenencia de la Fuerza
    F=[0,0,0,0,0]

    #SENTENCIAS DE LA TABLA FAM CADA GRUPO ES UNA COLUMNA DE LA TABLA

    #COLUMNA NG
    if ptita[0]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[0],pomega[0])
      F[4]=max(minimo,F[4])
    if ptita[0]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[0],pomega[1])
      F[4]=max(minimo,F[4])
    if ptita[0]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[0],pomega[2])
      F[4]=max(minimo,F[3])
    if ptita[0]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[0],pomega[3])
      F[3]=max(minimo,F[2])
    if ptita[0]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[0],pomega[4])
      F[2]=max(minimo,F[2])
    
    #COLUMNA NP
    if ptita[1]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[1],pomega[0])
      F[4]=max(minimo,F[4])
    if ptita[1]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[1],pomega[1])
      F[4]=max(minimo,F[3])
    if ptita[1]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[1],pomega[2])
      F[3]=max(minimo,F[3])
    if ptita[1]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[1],pomega[3])
      F[2]=max(minimo,F[1])
    if ptita[1]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[1],pomega[4])
      F[4]=max(minimo,F[1])

    #COLUMNA Z
    if ptita[2]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[2],pomega[0])
      F[4]=max(minimo,F[3])
    if ptita[2]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[2],pomega[1])
      F[4]=max(minimo,F[3])
    if ptita[2]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[2],pomega[2])
      F[2]=max(minimo,F[2])
    if ptita[2]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[2],pomega[3])
      F[1]=max(minimo,F[1])
    if ptita[2]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[2],pomega[4])
      F[0]=max(minimo,F[1])

   #COLUMNA PP
    if ptita[3]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[3],pomega[0])
      F[3]=max(minimo,F[3])
    if ptita[3]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[3],pomega[1])
      F[2]=max(minimo,F[2])
    if ptita[3]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[3],pomega[2])
      F[1]=max(minimo,F[1])
    if ptita[3]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[3],pomega[3])
      F[0]=max(minimo,F[1])
    if ptita[3]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[3],pomega[4])
      F[0]=max(minimo,F[0])

    #COLUMNA PG
    if ptita[4]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[4],pomega[0])
      F[2]=max(minimo,F[2])
    if ptita[4]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[4],pomega[1])
      F[0]=max(minimo,F[1])
    if ptita[4]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[4],pomega[2])
      F[0]=max(minimo,F[1])
    if ptita[4]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[4],pomega[3])
      F[0]=max(minimo,F[0])
    if ptita[4]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[4],pomega[4])
      F[0]=max(minimo,F[0])
    PF=F
    aux1=[0,0,0,0,0]
    
    #calculo por media de centros
    for i in range(5):
      if PF[i]!=0:
        conjunto=self.conjunto[i]
        centro=(conjunto[0]+conjunto[1])/2
        aux1[i]=centro*PF[i]
    if sum(aux1)!=0 and sum(PF)!=0:
      mediadc=sum(aux1)/sum(PF)
    else:
      mediadc=0
    return mediadc
   
def simular(t_max, delta_t, tita_0, v_0, a_0,it):
  tita = (tita_0 * np.pi) / 180
  v = v_0
  a = a_0
  vel=[]
  fuerza=[]
  dom = (90 * np.pi) / 180
  tita_dominio=(-dom,dom)
  tita_prima_dominio=(-6,6)
  fuerza_dominio=(-100,100)
  D1=difuso(tita_dominio)
  D2=difuso(tita_prima_dominio)
  D3=difuso(fuerza_dominio)
  CD1=D1.difuso_y()
  CD2=D2.difuso_y()
  CD3=D3.difuso_y()
 
  y = []
  x = np.arange(0, t_max, delta_t)
  f=0
  for t in x:
    a = calcula_aceleracion(tita, v, -f)
    v = v + a * delta_t
    vel.append(v)
    tita = tita + v * delta_t + a * np.power(delta_t, 2) / 2
    y.append(tita*180/np.pi)
    aux1=D1.valor_pertenencia(tita)
    aux2=D2.valor_pertenencia(v)
    f=D3.tabla(aux1,aux2)
    fuerza.append(f)

  #GRAFICAS
  
  fig,axs = plt.subplots(3,sharex=True,figsize=(10, 8))

  plt.suptitle("tmax="+str(t_max)+"s"+" | Δt="+str(delta_t)+"s"+" | θ(0)="+str(tita_0)+"°"+" | θ'(0)="+str(v_0)+"rad/s"+" | θ''(0)="+str(a_0)+"rad/s²")
  axs[0].grid(True)
  axs[0].plot(x, y,"r",label="θ")
  axs[0].legend(loc='upper left')
  axs[0].set_ylabel("[°]")
  axs[1].grid(True)
  axs[1].plot(x,fuerza,"black",label='Fuerza')
  axs[1].legend(loc='upper left')
  axs[1].set_ylabel("[N]")
  axs[2].grid(True)
  axs[2].plot(x, vel,label="θ'")
  axs[2].legend(loc='upper left')
  axs[2].set_ylabel("[rad/s]")
  axs[2].set_xlabel("tiempo [s]")
  

#EJEMPLOS A SIMULAR
simular(10, 0.0001, 90, 0, 0,1) #Limite sin velocidad
simular(10, 0.0001, 0, 0, 0,2)  #equilibrio sin velocidad
simular(10, 0.0001, 45, -1, 0,3)
simular(10, 0.0001, 45, 1, 0,4)
simular(10, 0.0001, 90, -3, 0,5)
simular(10, 0.0001, 90, 3, 0,6)

plt.show()
plt.ion()
