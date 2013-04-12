'''
Created on 2011-7-6

@author: terry
'''
class Column(object):
    def __init__(self):
        self.data = []
        self.desc = None
        self.tag = None
        
    def get_tag(self):
        if self.tag:
            return self.tag
        
        if self.desc.unit:
            self.tag= self.desc.name+"("+self.desc.unit+")"
        else:
            self.tag= self.desc.name
        return self.tag

class PlotData(object):
    def __init__(self):
        self.cols = {}
        self.data_meta = None
        
    def getByName(self,name):
        return self.cols.get(name,None)
        
    def load(self,src_data, data_meta, column_sep=" "):
        assert(data_meta)
        assert(src_data)
        self.data_meta = data_meta
        
        column_desc = data_meta.index_map.values()
        
        for x in column_desc:
            column = Column()
            column.desc = x
            self.cols[x.name] = column
        
        with open(src_data, "rb") as fIn:
            while True:
                line = fIn.readline()
                if not line: break
                line = line.strip()
                if not line: continue
                items = [x for x in line.split(column_sep) if x]
                
		if not items:
                    continue
                #print items
                for x in self.cols.values():
                    x.data.append(eval(items[x.desc.index]))
                    #print "load",x.desc.name,eval(items[x.desc.index])

def testPlotData():
    from datameta import DataMeta
    data_meta = DataMeta()
    data_meta.loadByFile("./test/datameta.xml")
    print data_meta
    plot_data = PlotData()
    plot_data.load("./test/data.txt", data_meta)
    
if __name__ == '__main__':
    testPlotData()
