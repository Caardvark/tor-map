from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import pandas as pd
import matplotlib.patheffects as PathEffects
from color_bar import plot_cbar

def plot_text(
m,v,fontsize=5,lwidth=1,
longmin=-18,latmin=30,longmax=33,latmax=70):
	"""Plots the numbers on the map
	some have bad placements (UK, Russia outside map...),
	so I had to manually adjust the dictionary containing the coordinates"""
	for i in v:
		if (
		v[i]["long"]>=longmin and v[i]["long"]<=longmax
		) and (
		v[i]["lat"]>=latmin and v[i]["lat"]<=latmax
		) or (
		i=="RU"
		):
			for i in v:
				x,y=m(
				v[i]["long"],
				v[i]["lat"]
				)
				txt=plt.text(x,y,str(v[i]["total servers"]),
				color='white',fontsize=fontsize, 
				horizontalalignment='center',
				verticalalignment='center')
				txt.set_path_effects([
				PathEffects.withStroke(
				linewidth=lwidth, foreground='k'
				)
				])

def get_values(df):
	"""Gets the latitude and longitude of country centroid, the short name,
	long name, and ISO 3166-2 designation for all countries"""
	s=df.loc[:,["Country Code"]]
	countries=pd.read_csv(
	"country_centroids_all.csv",
	sep="\t",
	header=0,
	index_col=None
	).loc[:,[
	"LAT","LONG","SHORT_NAME","FULL_NAME","ISO3136"
	]]
	cindex=countries.index
	maxindex=max(s.index.values)

	for i in s.index:
		for j in cindex:
			current_country=countries.loc[j,:]
			if (s.iat[i,0]==current_country["ISO3136"]):
				print "%d/%d servers processed..."%(i,maxindex)
				for k in ["LAT","LONG","SHORT_NAME","FULL_NAME"]:
					s=s.set_value(i,k,current_country[k])
	return s

def stats(series):
	"""Makes a dictionary with total number of servers and lat/long of countries"""
	d={}
	for index in series["Country Code"].unique():
		d[index]={
		"total servers" : len(series.loc[series["Country Code"]==index]),
		"lat" : series.loc[series["Country Code"]==index]["LAT"].iat[0],
		"long" : series.loc[series["Country Code"]==index]["LONG"].iat[0]
		}
	return d

def main(
	longmin=-8,latmin=30,longmax=55,latmax=70,
	proj="stere",show=False,save=False,cbar=False
	):
	#parameters for plotting the map

	m = Basemap(
		projection=proj,lat_0=45,lon_0=15,resolution='l',
		llcrnrlon=longmin,llcrnrlat=latmin,
		urcrnrlon=longmax,urcrnrlat=latmax,
		area_thresh = 1000)

	m.fillcontinents(color='#888888')

	shp_info = m.readshapefile('ne_10m_admin_0_countries',
					'states',drawbounds=True)

	#this can take a while...
	s=get_values(
	pd.read_csv("Tor_query_EXPORT.csv",header=0,index_col=None).loc[:100,:])
	s.dropna(how="any",inplace=True)

	v=stats(s)

	colors_states={}
	statenames=[]

	vmin = 0; vmax = max([i["total servers"] for i in v.values()]) # set range.

	interval = [vmin+k for k in np.linspace(vmin,vmax,num=len(colors)+1)] #set intervals

	for shapedict in m.states_info:
		isoname = shapedict['ISO_A2']
		wbname = shapedict['WB_A2'] #ISO 3166-2 and World Bank have (mostly) the same designation
		if isoname in v.keys():
			pop = v[isoname]["total servers"]

			#depending on value of pop, sets the color
			for k in range(len(interval)-1):
				if pop>=interval[k] and pop<=interval[k+1]:
					colors_states[isoname] = colors[k]
			statenames.append(isoname)
		elif wbname in v.keys():
			pop = v[wbname]["total servers"]

			for k in range(len(interval)-1):
				if pop>=interval[k] and pop<=interval[k+1]:
					colors_states[wbname] = colors[k]
			statenames.append(wbname)
		elif shapedict["NAME"]=="Norway": #Norway isn't found for some reason
			try:
				pop = v["NO"]["total servers"]

				for k in range(len(interval)-1):
					if pop>=interval[k] and pop<=interval[k+1]:
						colors_states["NO"] = colors[k]
			except:
				pass

				statenames.append("NO")
		else:
			colors_states[wbname] = "888888"
			statenames.append(wbname)

	ax = plt.gca()

	for nshape,seg in enumerate(m.states):
		try:
			if statenames[nshape] in v.keys():
				color = colors_states[statenames[nshape]]
				poly = Polygon(seg,facecolor=color,
						edgecolor=color,linewidth=0.05)
				ax.add_patch(poly)
			else:
				color =  "888888"
				poly = Polygon(seg,facecolor=color,
						edgecolor=color,linewidth=0.05)
				ax.add_patch(poly)
		except:
			pass

	plt.title('Tor services in Europe\nTotal worldwide: %d'%len(s))
	plot_text(m,v)

	source1="https://torstatus.blutmagie.de/"
	source2="http://www.naturalearthdata.com/downloads/10m-cultural-vectors/"
	source3="http://gothos.info/resources/"

	txt=plt.annotate("Sources:\n%s\n%s\n%s"%(source1,source2,source3),xy=(0.0,-0.05),
			color="white",fontsize=5,xycoords="axes fraction",
			verticalalignment='center', horizontalalignment='left')

	txt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='k')])

	if save==True:
		plt.savefig("output.png",dpi=500)
	if show==True:
		plt.show()
	plt.close("all")
	if cbar==True:
		plot_cbar(interval,colors,show=True)


colors=[
"#67001f","#b2182b","#d6604d","#f4a582","#fddbc7",
"#d1e5f0","#92c5de","#4393c3","#2166ac","#053061"
]

main(show=True,save=True,cbar=True)

