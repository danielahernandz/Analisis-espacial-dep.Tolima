#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
import os


# In[8]:


os.chdir('C:\\Users\\isabe\\OneDrive\Escritorio\python')


# In[9]:


#Cargas base de datos
viviendas=pd.read_csv('vivienda_nueva_bta.csv')


# In[10]:


viviendas


# In[14]:


viviendas.rename(columns={'Latitud':'lon','Longitud':'lat'}, inplace=True)
viviendas['geometry']=viviendas[['lon','lat']].apply(Point, axis=1)


# In[15]:


type(viviendas)


# In[20]:


viviendas=gpd.GeoDataFrame(viviendas)
viviendas.crs={'init': 'epsg:4326'}


# In[21]:


viviendas.plot()


# In[22]:


#Cargar el shape de Bogotá
shp_bog = gpd.read_file('Loca.shp')
#Definir sistema de coordenadas
shp_bog.crs={'init': 'epsg:4326'}


# In[23]:


type(shp_bog)


# In[24]:


shp_bog.plot()


# In[26]:


shp_bog.columns


# In[28]:


#Eliminar sumpaz
shp_bog=shp_bog[shp_bog['LocNombre'] !='SUMAPAZ']


# In[29]:


shp_bog.plot()


# In[30]:


#Graficar en la misma figura las localidades de bogota y los datos de vivienda nueva
fig, ax=plt.subplots(figsize=(8,12))
shp_bog.plot(ax=ax, color='lightgrey',edgecolor='k')
viviendas.plot(ax=ax)


# In[31]:


#Union de varias geometrias en una sola 
import shapely.ops as ops


# In[32]:


#Unir las diferentes localidades para crear el poligono de bgta
bogota=ops.cascaded_union(shp_bog['geometry'])


# In[33]:


bogota


# In[34]:


type(bogota)


# In[35]:


#viviendas.intersects(bogota) <- Nos dice si los proyectos de vivienda estan en ngta o no
#viviendas[viviendas.intersects(bogota)] <- Nos quedamos cons los registros para los cuales el intercepto de viviendas.intersects sea true
viviendas=viviendas[viviendas.intersects(bogota)]


# In[36]:


viviendas


# In[37]:


viviendas.plot()


# In[38]:


fig, ax=plt.subplots(figsize=(8,12))
viviendas.plot(ax=ax, color='lightgrey',edgecolor='k')
viviendas.plot(ax=ax)


# In[39]:


from matplotlib import colors


# In[40]:


cmap= colors.ListedColormap(['green','red','blue'])

                            
                            
                           


# In[41]:


#Crear una figura
fig, ax=plt.subplots(figsize=(8,12))
#Graficar las localidades de Bogotá con fondo gris y fondos negros (Ubicar en ax)
shp_bog.plot(ax=ax, color='lightgrey', edgecolor='k')
#Graficar los proyectos inmobiliarios (Asignar colores con la paleta que creamos)
viviendas.plot(ax=ax, column='Tipo_vivienda', cmap=cmap, markersize=5, categorical=True, legend=True, legend_kwds={'loc':'lower right'})
#Eliminar ejes
ax.axis('off')


# In[42]:


#Ver documentación
get_ipython().run_line_magic('pinfo', 'gpd.sjoin')
#Un merge especial de las bases de datos,por defecto con la operacion intersects
#En nuestro caso lo que haremos es asignar para cada localidad los proyectos de vivienda.
#Por defecto se conserva la geometria base de datos (en nuestro caso, localidades)


# In[43]:


viviendas_loc=gpd.sjoin(shp_bog,viviendas, how='inner')


# In[44]:


viviendas_loc


# In[46]:


#Contar el número de proyectos para cada localidad
viviendas_loc=viviendas_loc.groupby('LocCodigo').size().reset_index(name='proyectos')


# In[47]:


viviendas_loc


# In[50]:


#Pegar a cada localidad el número de proyectos inmobiliarios encontrados
viviendas_loc=shp_bog.merge(viviendas_loc, on = 'LocCodigo',how='left')


# In[51]:


viviendas_loc


# In[52]:


#Rellenar con 0 para aquella localidades que no tienen proyectos asignados.
viviendas_loc.fillna({'proyectos':0},inplace=True)


# In[53]:


viviendas_loc


# In[ ]:





# In[ ]:




