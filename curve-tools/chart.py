'''
Created on 2011-7-5

@author: terry
'''
import os

    

def load_data(src, col_num=10):
    #import time
    data = []
    rangeX = range(col_num)
    for x in rangeX:
        data.append([])
    #start_ts = 0
    with open(src) as fin:
        for line in fin.readlines():
            if not line:
                continue
            line = line.strip()
            items = [x for x in line.split(" ") if x]
            if len(items)<col_num: continue
            for x in rangeX:
                data[x].append(eval(items[x]))
            #if not start_ts:
            #    start_ts = data[0][0]
            #if start_ts:
            #    data[0][-1] = (data[0][-1]-start_ts)/1000
            #data[0][-1] = data[0][-1]/(24*3600*1000.0)
            #print data[0][-1],time.ctime(data[0][-1])
                #print "Append",x,items[x]
    return data


def align(x,y,count=20,tick=10):
    delta = (y-x)/count
    x = x - delta
    #if x<0:
    #    x = 0
    y = y + delta
    return range(x,y ,(y-x)/count)   

def test_plot(data,cols={"dAvgTh":(-2,None),"tAvgTh":(-1,None)},figure_name="throughtput",xtag="time",ytag=None,index=0,out_dir="pics"):
    index_data = data[index]
    
    #group ths
    ths = {}
    oths={}
    for k,v in cols.items():
        if k.lower().endswith("avgth"):
            ths[k] = v
        else: 
            oths[k] = v
    ths_Y = (int(min([min(data[x[0]]) for x in ths.values()])),
             int(max([max(data[x[0]]) for x in ths.values()])))  
        
    oths_Y = (int(min([min(data[x[0]]) for x in oths.values()])),
             int(max([max(data[x[0]]) for x in oths.values()]))) 
    
    import matplotlib.pyplot as plt

    count = 0
    if ths:
        count+=1
    if oths:
        count+=1
    
    if count==2:
        fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True, sharey=False)  
    else:
        fig, ((ax1, ), ) = plt.subplots(1, 1, sharex=False, sharey=False)  
    
    fig.set_figheight(6)
    fig.set_figwidth(8)
    
    colors = "bgrcmyk"
    color_idx = 0

    ax1.set_axisbelow(True)
    
    
    #print x[0]

    
    lines = []
    tags = []

    if ths:
        if ytag:
            ax1.set_ylabel("ops/sec")
        if xtag:
            ax1.set_xlabel(xtag)    
                
        for k,v in ths.items():
            if v[1]:
                tags.append(k+" ("+v[1]+")")
            else:
                tags.append(k)
            lines.append(ax1.plot(index_data,data[v[0]],linestyle='solid',color=colors[color_idx%len(colors)],lw=2))
            color_idx+=1
        ax1.set_yticks(align(ths_Y[0],ths_Y[1]))
        
        ax1.legend(lines,  tags, loc=0)
        ax1.grid(True)
    else:
        ax2 = ax1

    lines = []
    tags = []        
    if oths:
        for k,v in oths.items():
            if v[1]:
                tags.append(k+" ("+v[1]+")")
            else:
                tags.append(k)
            lines.append(ax2.plot(index_data,data[v[0]],linestyle='solid',color=colors[color_idx%len(colors)],lw=2))
            color_idx+=1  
        ax2.set_yticks(align(oths_Y[0],oths_Y[1]))      
        ax2.legend(lines,  tags, loc=0)
        ax2.grid(True)
        for label in ax2.get_xticklabels():
            label.set_visible(False)
        #ax1.autoscale_view()
    if figure_name: fig.suptitle(figure_name)
     
    fig.savefig(os.path.join(out_dir,figure_name+'.png'),dpi=100)
    
    fig.clear()
    #new_figure_manager, draw_if_interactive, show = pylab_setup() 

def test_plot2(data,cols={"dAvgTh":(-2,None),"tAvgTh":(-1,None)},figure_name="throughtput",xtag="time",ytag=None,index=0,out_dir="pics"):
    index_data = data[index]
    #group ths
    ths = {}
    oths={}
    for k,v in cols.items():
        if k.lower().endswith("avgth"):
            ths[k] = v
        else: 
            oths[k] = v
    ths_Y = (int(min([min(data[x[0]]) for x in ths.values()])),
             int(max([max(data[x[0]]) for x in ths.values()])))  
        
    oths_Y = (int(min([min(data[x[0]]) for x in oths.values()])),
             int(max([max(data[x[0]]) for x in oths.values()]))) 
    
    from matplotlib.pylab import figure

    count = 0
    if ths:
        count+=1
    if oths:
        count+=1
    
    fig = figure()
    ax1 = fig.add_subplot(111)
    
    fig.set_figheight(6)
    fig.set_figwidth(8)
    
    colors = "bgrcmyk"
    color_idx = 0

    ax1.set_axisbelow(True)
    
    lines = []
    tags = []

    if ths:
        if ytag:
            ax1.set_ylabel("ops/sec")
        if xtag:
            ax1.set_xlabel(xtag)    
                
        for k,v in ths.items():
            if v[1]:
                tags.append(k+" ("+v[1]+")")
            else:
                tags.append(k)
            lines.append(ax1.plot(index_data,data[v[0]],linestyle='solid',color=colors[color_idx%len(colors)],lw=2))
            color_idx+=1
        ax1.set_yticks(align(ths_Y[0],ths_Y[1]))
        #ax1.set_ylim(ths_Y[0],ths_Y[1])
        #ax1.legend(lines,  tags, loc=0)
        for label in ax1.xaxis.get_ticklabels():
            # label is a Text instance
            #label.set_color('red')
            label.set_rotation(30)
            label.set_fontsize(8)
            
        ax1.grid(True)
        ax2 = ax1.twinx()
    else:
        ax2 = ax1

    #lines = []
    #tags = []        
    if oths:
        for k,v in oths.items():
            if v[1]:
                tags.append(k+" ("+v[1]+")")
            else:
                tags.append(k)
            lines.append(ax2.plot(index_data,data[v[0]],linestyle='solid',color=colors[color_idx%len(colors)],lw=2))
            color_idx+=1  
        ax2.set_yticks(align(oths_Y[0],oths_Y[1]))  
        #ax2.set_ylim(oths_Y[0],oths_Y[1])
        leg = ax2.legend(lines,  tags, loc=0)
        leg.get_frame().set_alpha(0.1)
        ax2.grid(True)
        #ax1.autoscale_view()
    if figure_name: fig.suptitle(figure_name)
     
    fig.savefig(os.path.join(out_dir,figure_name+'.png'),dpi=100)
    
    fig.clear()

def draw_pic(src,dst_prefix):
    data = load_data(src)
    test_plot2(data,{"dAvgTh":(-2,"ops/sec"),"tAvgTh":(-1,"ops/sec"),"dMaxLat":(3,"ms"),"dAvgLat":(4,"ms")},figure_name=dst_prefix,xtag="time",)
    
if __name__ == '__main__':
    src_dir = r'D:\study\java\rock_test\merged_result'
    dirs = os.listdir(src_dir)
    for sub_dir in dirs:
        draw_pic(os.path.join(os.path.join(src_dir,sub_dir),"all_put_th.txt"),sub_dir)
    print src_dir
    pass