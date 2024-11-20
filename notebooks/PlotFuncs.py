
from numpy import *
from numpy.random import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib.ticker
from matplotlib.colors import ListedColormap
from matplotlib import colors
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
from scipy.stats import norm
import matplotlib.patheffects as pe

# Save PDF and PNG versions of figure at the same time
pltdir = '../plots/'
pltdir_png = pltdir+'/plots_png/'
def MySaveFig(fig,pltname,pngsave=True):
    fig.savefig(pltdir+pltname+'.pdf',bbox_inches='tight')
    if pngsave:
        fig.set_facecolor('w')
        fig.savefig(pltdir_png+pltname+'.png',bbox_inches='tight',transparent=False)


# Main function for plotting and labelling a bound
def PlotBound(ax,filename,
            edgecolor='k',facecolor='crimson',facealpha=1,edgealpha=1,lw=3,zorder=0.1,hatch=None,linestyle='-',path_effects=[pe.Stroke(linewidth=5, foreground='k'), pe.Normal()],
            y2=1e10,skip=1,rescale_m=False,scale_x=1,scale_y=1,start_x=0,end_x=nan,MinorEdgeScale=1.5,AddMinorEdges=False,
            label=None,label_pos=[0,0],textcolor='k',text_path_effects=[pe.Stroke(linewidth=1, foreground='k'), pe.Normal()],textalpha=1,rotation=0,fontsize=25):
   
    # ax = axis object to add the bound to
    # filename = name of file including path containing the data to plot, assumed that xaxis = first column and yaxis = second column

    # Bound appearance options:
    # edgecolor = color of the edge of the bound
    # facecolor = color to fill in the area of the bound
    # facealpha = transparency of the fill
    # edgealpha = transparency of the edge
    # lw = linewidth
    # zorder = zorder of all plot objects added
    # hatch = e.g. '/' for filling the bound with a hatch effect
    # linestyle = e.g. '--', ':' etc.
    # path_effects = path effects for the bound edge

    # Customise how bound is plotted:
    # y2 = y2 parameter is used by plt.fill_between(), if you want to plt.fill() instead then use y2=nan
    # rescale_m = switch to True if second column (i.e. coupling or cross section) needs to be rescaled by 1/m
    # skip = how many entries of data file to skip, e.g. skip=2 will plot every other data point. This is useful if the bound is very spiky
    # start_x = row of datafile to start plotting
    # end_x = row of datafile to stop plotting
    # scale_x = rescale first column of datafile by some amount
    # scale_y = rescale second column of datafile by some amount
    # AddMinorEdges = switch to True if you don't want the bound shooting up to the top of the plot when the coupling or cross section = infinity

    # Label options:
    # label = best to use a raw string to render latex correctly, e.g. r'$\pi$'
    # fontsize 
    # rotation = rotation of textlabel on the plot
    # label_pos = [x,y] position on the plot where label should be
    # textalpha = transparency of text label
    # text_path_effects = path_effects for text label
   
    dat = loadtxt(filename)
    if end_x/end_x==1:
        dat = dat[start_x:end_x,:]
    else:
        dat = dat[start_x:,:]
    dat[:,0] *= scale_x
    dat[:,1] *= scale_y
    if rescale_m:
        dat[:,1] = dat[:,1]/dat[:,0]
    if isnan(y2):
        ax.fill(dat[0::skip,0],dat[0::skip,1],color=facecolor,alpha=facealpha,zorder=zorder,lw=0,hatch=hatch)
    else:
        ax.fill_between(dat[0::skip,0],dat[0::skip,1],y2=y2,color=facecolor,alpha=facealpha,zorder=zorder,lw=0,hatch=hatch)

    if lw>0:
        ax.plot(dat[0::skip,0],dat[0::skip,1],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha,path_effects=path_effects)
    if skip>1:
        ax.plot([dat[-2,0],dat[-1,0]],[dat[-2,1],dat[-1,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
    if AddMinorEdges:
        ax.plot([dat[-1,0],dat[-1,0]],[dat[-1,1],MinorEdgeScale*dat[-1,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha,path_effects=path_effects)
        ax.plot([dat[0,0],dat[0,0]],[dat[0,1],MinorEdgeScale*dat[0,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha,path_effects=path_effects)

    if label:
        plt.text(label_pos[0],label_pos[1],label,fontsize=fontsize,
                color=textcolor,rotation=rotation,path_effects=text_path_effects,clip_on=True,alpha=textalpha,rotation_mode='anchor')
    return

def line_background(lw,col):
    # How to use: 
    # Do plt.plot(x,y,'r-',lw=2,path_effects=line_background(4,'k)) to plot a red line with a black outline
    return [pe.Stroke(linewidth=lw, foreground=col), pe.Normal()]

    
def SimpleAnnotation(ax,x1,x2,y1,y2,color='red',lw=3,path_effects=line_background(4,'k'),marker='o',markersize=7,mec='k',mew=1):
    # Plots a simple line between [x1,y1] and [x2,y2] with a small marker at [x2,y2]
    ax.plot([x1,x2],[y1,y2],color=color,lw=lw,path_effects=path_effects)
    ax.plot(x2,y2,marker,markersize=markersize,mec='k',mew=mew,mfc=color)
    return


def cbar(mappable,extend='neither',minorticklength=8,majorticklength=10,\
            minortickwidth=2,majortickwidth=2.5,pad=0.2,side="right",orientation="vertical"):
    # Custom colobrar that does not do matplotlib's annoying thing where colorbars change the size of a figure
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(side, size="5%", pad=pad)
    cbar = fig.colorbar(mappable, cax=cax,extend=extend,orientation=orientation)
    cbar.ax.tick_params(which='minor',length=minorticklength,width=minortickwidth)
    cbar.ax.tick_params(which='major',length=majorticklength,width=majortickwidth)
    cbar.solids.set_edgecolor("face")
    return cbar


def CreateEnvelope(fpath,file_list,new_file_name,m_min,m_max,nm=1000,header='DM Mass    cross section'):
    # Use this to create an envelope of many data files, e.g. for combining the best limits over some mass range between m_min and m_max
    mvals = logspace(log10(m_min),log10(m_max),nm)
    g = zeros(shape=nm)
    for file in file_list:
        dat = loadtxt(fpath+file+".txt")
        g1 = 10**interp(log10(mvals),log10(dat[:,0]),log10(dat[:,1]))
        g1[mvals<amin(dat[:,0])] = inf
        g1[mvals>amax(dat[:,0])] = inf
        g = column_stack((g,g1))
    g = g[:,1:]
    g = amin(g,1)
    g[g==inf] = 1
    savetxt(fpath+new_file_name+'.txt',column_stack((mvals,g)),header=header)
    return


def UpperAxis_grams(ax,tickdir='out',xtick_rotation=0,labelsize=25,xlabel=None,lfs=40,tick_pad=8,tfs=25,xlabel_pad=10):
    m_min,m_max = ax.get_xlim()
    GeV_2_g = 1/5.62e23 # convert GeV to grams
    ax2 = ax.twiny()
    ax2.set_xscale('log')
    ax2.set_xlabel(xlabel,fontsize=lfs,labelpad=xlabel_pad)
    ax2.tick_params(labelsize=tfs)
    ax2.tick_params(which='major',direction=tickdir,width=2.5,length=13,pad=tick_pad)
    ax2.tick_params(which='minor',direction=tickdir,width=1,length=10)

    #ax2.xaxis.set_major_locator(matplotlib.ticker.LogLocator(base=1000,subs=(1.0,),numticks=100))
    #ax2.xaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10,subs=(1.0,),numticks=100))

    ax2.set_xticks(10.0**arange(-18,18,3))
    ax2.set_xticklabels(['ag','fg','pg','ng',r'\textmu g','mg','g','kg','Mg','Gg','Tg','Pg']);
    ax2.set_xticks(10.0**arange(-18,18-2,1), minor=True)
    ax2.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax2.set_xlim([m_min*GeV_2_g,m_max*GeV_2_g])
    plt.sca(ax)
    return


def col_alpha(col,alpha=0.1):
    # col_alpha('red',0.5) will create a new colour that looks like the colour 'red' with an alpha of 0.5 but without actually being transparent
    rgb = colors.colorConverter.to_rgb(col)
    bg_rgb = [1,1,1]
    return [alpha * c1 + (1 - alpha) * c2
            for (c1, c2) in zip(rgb, bg_rgb)]


def reverse_colourmap(cmap, name = 'my_cmap_r'):
    # Creates a reverse colourmap out of cmap
    reverse = []
    k = []
    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))
    LinearL = dict(zip(k,reverse))
    my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r