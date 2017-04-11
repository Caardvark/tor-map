import matplotlib.pyplot as plt
import matplotlib as mpl


#-------------------------------------------------------------------------------

#Basically a modified version of
#https://matplotlib.org/examples/api/colorbar_only.html

#-------------------------------------------------------------------------------

# Make a figure and axes with dimensions as desired.

def plot_cbar(interval,colors,save=False,show=False):
	fig = plt.figure(figsize=(3, 5))
	ax = fig.add_axes([0.4, 0.2,0.15 , 0.7])

	cmap = mpl.cm.cool
	norm = mpl.colors.Normalize(vmin=5, vmax=10)

	cmap = mpl.colors.ListedColormap(colors)
	cmap.set_over((1., 0., 0.))
	cmap.set_under((0., 0., 1.))

	bounds = interval
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
		                        norm=norm,
		                        extendfrac='auto',
		                        ticks=bounds,
		                        spacing='uniform',
		                        orientation='vertical')
	cb.set_label('Number of services')
	if save==True:
		plt.savefig("colorbar.png",dpi=200)
	if show==True:
		plt.show()
	plt.close("all") #might report warnings


