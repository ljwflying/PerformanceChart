'''
Created on 2011-7-8

@author: terry
'''

import os
from matplotlib.pyplot import figure
from multiprocessing import Pool

            
class PlotTool:
    def __init__(self):
        #self.clear()
        self.plot_meta_src = None
        self.plot_meta = None
        self.data_meta = None
        self.plot_data = None
    
    def clear(self):
        if self.plot_meta_src:
            del self.plot_meta_src
            del self.plot_meta
            del self.data_meta
            del self.plot_data
    
    def load(self, plot_meta_src):
        self.plot_meta_src = plot_meta_src
        self.__load_plotmeta()
        self.__load_datameta()
        self.__load_plotdata()
    
    def __check_exists(self,path):
        if os.path.exists(path) and os.path.isfile(path):
            return True
        else:
            raise Exception("file %s is not existed or not a regular file"%(path))
        
    def __load_plotmeta(self):
        self.__check_exists(self.plot_meta_src)
        from plotmeta import PlotMeta
        self.plot_meta = PlotMeta()
        self.plot_meta.loadByFile(self.plot_meta_src)
        print "load plot meta data ok!"
    
    def __load_datameta(self):
        data_meta_list = self.plot_meta.datameta
        self.data_meta = {}
        from datameta import DataMeta
        for entry in data_meta_list:
            src = entry["source"][0]
            self.__check_exists(src)
            data_meta = DataMeta()
            data_meta.loadByFile(src)
            self.data_meta[entry["name"][0]] = data_meta
        assert(self.data_meta)
        print "load data meta data ok!"
    
    @staticmethod
    def convert_linesep(linesep):
        linesep = linesep.strip()
        linesep = linesep.replace("~tab", "\t")
        linesep = linesep.replace("~space"," ")
        
        return linesep
    
    def __load_plotdata(self):
        plot_data_list =self.plot_meta.plotdata
        self.plot_data = {}
        from plotdata import PlotData
        for entry in plot_data_list:
            src = entry["source"][0]
            self.__check_exists(src)
            data_meta = self.data_meta[entry["meta"][0]]
            assert(data_meta)
            name = entry["name"][0]
            assert(not self.plot_data.has_key(name))
            plot_data = PlotData()
            plot_data.load(src, data_meta, PlotTool.convert_linesep(entry.get("linesep",["~space",])[0]))
            self.plot_data[name] = plot_data
        assert(self.plot_data)
        print "load plot data ok!"
        
    def align(self,x,y,count=20,tick=10):
        delta = (y-x)/count
        if not delta:
            delta = 1
            
        if x>delta:
            x = x - delta
            
        y = y + delta
        ret = [x]
        v = x

        while v<=y:
            v+= delta
            ret.append(v) 
        return ret   
         
    def draw(self):
        for plot_x in self.plot_meta.plot:
            """
                        <plot>
                            <output>./test/throughtput.png</output>
                            <title>throughtput</title>
                            <data>all_throughtput</data>
                            <index> time </index>
                            <series>  dAvgTh </series>
                            <series> tAvgTh</series>
                            <xlabel> time </xlabel>
                            <ylabel> ops/sec </ylabel>    
                            <xticknum>20</xticknum>  
                            <yticknum>20</yticknum>
                            <xrotation>0</xrotation>
                            <legendalpha>0.1</legendalpha>  
                            <height>6</height>
                            <width>8</width>
                            <dpi>100</dpi>                       
                        </plot>
            """          
            output = plot_x["output"][0]
            if os.path.exists(output) and os.path.isdir(output):
                raise Exception("output file"+output+" existed, but it is a directory!")
            parent_dir = os.path.dirname(output)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            
            plot_data = self.plot_data.get(plot_x["data"][0])
            assert(plot_data)
            index_data = plot_data.getByName(plot_x["index"][0]).data
            #print index_data
            assert(index_data)
            series = [plot_data.getByName(series_name) 
                      for series_name in plot_x["series"]]
            legend_labels = [x.get_tag() for x in series]
            #print legend_labels
            assert(series)
            
            x_ticks = self.align(min(index_data), 
                                 max(index_data), 
                                 int(plot_x.get("xticknum",[10,])[0]))
            x_label = plot_x.get("xlabel",["",])[0]
            y_label = plot_x.get("ylabel",["",])[0]
            
            y_ticks = self.align(min([min(s.data) for s in series]),
                                 max([max(s.data) for s in series]),
                                int(plot_x.get("yticknum",[10,])[0]))
            
            fig = figure()
            fig.set_figheight(int(plot_x.get("height",[6,])[0]))
            fig.set_figwidth(int(plot_x.get("width",[8,])[0]))
            
            ax1 = fig.add_subplot(111)
            colors = "bgrcmyk"
            marks = ['-',	#solid line style
                    '--', 	#dashed line style
                    '-.', 	#dash-dot line style
                    ':' ,	#dotted line style
                    '.', 	#point marker
                    ',', 	#pixel marker
                    'o' ,	#circle marker
                    'v' ,	#triangle_down marker
                    '^' ,	#triangle_up marker
                    '<' ,	#triangle_left marker
                    '>' ,	#triangle_right marker
                    '1' ,	#tri_down marker
                    '2' ,	#tri_up marker
                    '3' ,	#tri_left marker
                    '4' ,	#tri_right marker
                    's' ,	#square marker
                    'p' ,	#pentagon marker
                    '*' ,	#star marker
                    'h' ,	#hexagon1 marker
                    'H' ,	#hexagon2 marker
                    '+' ,	#plus marker
                    'x' ,	#x marker
                    'D' ,	#diamond marker
                    'd' ,	#thin_diamond marker
                    '|' ,	#vline marker
                    '_' ,	#hline marker
                     ]
            color_idx = 0            
            
            lines = []
            for s in series:
                lines.append(ax1.plot(index_data,s.data,linestyle='solid',color=colors[color_idx%len(colors)],marker=marks[color_idx%len(marks)],lw=2))
                color_idx+=1
            ax1.set_yticks(y_ticks)
            ax1.set_xticks(x_ticks)

            x_font = int(plot_x.get("xfontsize",["8",])[0])
            if x_font:
                for label in ax1.xaxis.get_ticklabels():
                        label.set_fontsize(x_font)
                        
            x_rotation = int(plot_x.get("xrotation",['0',])[0])        
            if x_rotation:
                for label in ax1.xaxis.get_ticklabels():
                    label.set_rotation(x_rotation)
                    label.set_fontsize(8)
                
            ax1.grid(True)

            leg = ax1.legend(lines,  legend_labels, loc=0)
            leg.get_frame().set_alpha(float(plot_x.get("legendalpha",["0.1",])[0]))
                            
            if y_label:
                ax1.set_ylabel(y_label)
            if x_label:
                ax1.set_xlabel(x_label)  
                
            title = plot_x.get("title",["",])[0]
            if title: fig.suptitle(title)
         
            fig.savefig(output,dpi=int(plot_x.get("dpi",[100,])[0]))
            fig.clear()
            del fig
            print "draw",output,"ok"

import os

def pic_draw(path):
    f = os.path.abspath(path)
    d = os.path.dirname(f)
    okF = os.path.join(d,"ok2.txt")
    
    print "process",path
    if os.path.exists(okF):
        print "draw dir",path,"ok"
        return 0
    plot_tool = PlotTool()
    plot_tool.load(path)
    plot_tool.draw()
    plot_tool.clear()

    with open(okF,"wb") as fout:
        fout.write("ok!")
    print "draw dir",path,"ok"
    return 0

if __name__ == '__main__':
    
#    tasks = ["./data/1NIC-1DataNode-1Storage/plotmeta.xml",
#             "./data/1NIC-1DataNode-1Storage/plotmeta.xml",
#             "./data/1NIC-1DataNode-1Storage-1replica/plotmeta.xml",
#             "./data/1NIC-1DataNode-2Storage/plotmeta.xml",
#             "./data/1NIC-1DataNode-2Storage-1replica/plotmeta.xml",
#            "./data/1NIC-1DataNode-3Storage/plotmeta.xml",
#            "./data/1NIC-1DataNode-3Storage-1replica/plotmeta.xml",
#             "./data/2NIC-2DataNode-2Storage/plotmeta.xml",
#            "./data/2NIC-2DataNode-2Storage-1replica/plotmeta.xml",
#             "./data/3NIC-3DataNode-3Storage/plotmeta.xml",
#             "./data/3NIC-3DataNode-3Storage-1replica/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-1Storage/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-1Storage-1replica/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-2Storage/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-2Storage-1replica/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-3Storage/plotmeta.xml",
#             "./data/bonding-3NIC-1DataNode-3Storage-1replica/plotmeta.xml",
#            ]
#    tasks = ["./data/data-6-4K-m/plotmeta.xml",
#             "./data/data-6-64K-m/plotmeta.xml",
#             "./data/data-6-2M-m/plotmeta.xml",
#             "./data/data-9-4K-m/plotmeta.xml",
#             "./data/data-9-64K-m/plotmeta.xml",
#             "./data/data-9-2M-m/plotmeta.xml",
#             "./data/data-12-4K-m/plotmeta.xml",
#             "./data/data-12-64K-m/plotmeta.xml",
#             "./data/data-12-2M-m/plotmeta.xml",
#             "./data/data-15-4K-m/plotmeta.xml",
#             "./data/data-15-64K-m/plotmeta.xml",
#             "./data/data-15-2M-m/plotmeta.xml",
#             "./data/DataNode-base-ex-mix/plotmeta.xml"
#             ]
#    tasks = ["./data/ohive-4K-40-wr/plotmeta.xml",
#             "./data/ohive-4K-100-wr/plotmeta.xml",
#             "./data/ohive-8K-40-wr/plotmeta.xml",
#             "./data/ohive-8K-100-wr/plotmeta.xml",
#             "./data/ohive-64K-40-wr/plotmeta.xml",
#             "./data/ohive-64K-100-wr/plotmeta.xml",
#             "./data/ohive-5M-40-wr/plotmeta.xml",
#             ]
    
    tasks = ["./all-result/4096-20000-62-1st/plotmeta.xml",
             "./all-result/8192-10000-62-3st/plotmeta.xml",
             "./all-result/65536-2000-62-5st/plotmeta.xml",
             "./all-result/5242880-40-62-7st/plotmeta.xml",
             "./all-result/r-4096-2000-62-1st/plotmeta.xml",
             "./all-result/r-8192-1000-62-3st/plotmeta.xml",
             "./all-result/r-65536-1000-62-5st/plotmeta.xml",
             "./all-result/r-5242880-40-62-7st/plotmeta.xml",
             ]

    for t in tasks:
        pic_draw(t)

    #pool = Pool(processes=len(tasks))
    #resultSet = [x.get() for x in [pool.apply_async(pic_draw, (task,)) for task in tasks]]
    #print resultSet

    
