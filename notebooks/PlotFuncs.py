
from numpy import *
from numpy.random import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib import colors
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
from scipy.stats import norm
import matplotlib.patheffects as pe

pltdir = '../plots/'
pltdir_png = pltdir+'/plots_png/'

def MySaveFig(fig,pltname,pngsave=True):
    fig.savefig(pltdir+pltname+'.pdf',bbox_inches='tight')
    if pngsave:
        fig.set_facecolor('w')
        fig.savefig(pltdir_png+pltname+'.png',bbox_inches='tight',transparent=False)


def PlotBound(ax,filename,edgecolor='k',facecolor='crimson',facealpha=1,lw=3,y2=1e10,zorder=0.1,hatch=None,
              linestyle='-',skip=1,edgealpha=1,rescale_m=False,textcolor='k',
              scale_x=1,scale_y=1,start_x=0,end_x=nan,MinorEdgeScale=1.5,AddMinorEdges=False,path_effects=[pe.Stroke(linewidth=5, foreground='k'), pe.Normal()],
              label =None,label_pos=[0,0],text_on=False,
              text_path_effects=[pe.Stroke(linewidth=1, foreground='k'), pe.Normal()],textalpha=1,rotation=0,fontsize=25):
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
        ax.plot([dat[-1,0],dat[-1,0]],[dat[-1,1],MinorEdgeScale*dat[-1,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)
        ax.plot([dat[0,0],dat[0,0]],[dat[0,1],MinorEdgeScale*dat[0,1]],color=edgecolor,zorder=zorder,lw=lw,linestyle=linestyle,alpha=edgealpha)

    if label:
        plt.text(label_pos[0],label_pos[1],label,fontsize=fontsize,
                color=textcolor,rotation=rotation,path_effects=text_path_effects,clip_on=True,alpha=textalpha,rotation_mode='anchor')
    return

def line_background(lw,col):
    return [pe.Stroke(linewidth=lw, foreground=col), pe.Normal()]


def cbar(mappable,extend='neither',minorticklength=8,majorticklength=10,\
            minortickwidth=2,majortickwidth=2.5,pad=0.2,side="right",orientation="vertical"):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(side, size="5%", pad=pad)
    cbar = fig.colorbar(mappable, cax=cax,extend=extend,orientation=orientation)
    cbar.ax.tick_params(which='minor',length=minorticklength,width=minortickwidth)
    cbar.ax.tick_params(which='major',length=majorticklength,width=majortickwidth)
    cbar.solids.set_edgecolor("face")

    return cbar


def col_alpha(col,alpha=0.1):
    rgb = colors.colorConverter.to_rgb(col)
    bg_rgb = [1,1,1]
    return [alpha * c1 + (1 - alpha) * c2
            for (c1, c2) in zip(rgb, bg_rgb)]


def reverse_colourmap(cmap, name = 'my_cmap_r'):
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