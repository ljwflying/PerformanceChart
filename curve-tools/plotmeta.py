'''
Created on 2011-7-6

@author: terry
'''
import xml.sax
from xml.sax.handler import ContentHandler
import os

class PlotMetaHandler(ContentHandler):
    """ parse plot meta"""
    SAMPLE_XML = """<?xml version="1.0" encoding="utf-8"?>
                    <configure>
                        <datameta>
                            <name>throughtput</name>
                            <source>./test/throughtput_datameta.xml</source>
                        </datameta>
                        
                        <datameta>
                            <name>delay</name>
                            <source>./test/delay_datameta.xml</source>
                        </datameta>    
                        
                        <plotdata>
                            <name>all_throughtput</name>
                            <meta>throughtput</meta>
                            <source>./test/throughtput_data.txt</source>
                            <!-- ~tab/~space/xxxx -->
                            <linesep>tab</linesep>
                        </plotdata>
                        
                        <plotdata>
                            <name>all_delay</name>
                            <meta>throughtput</meta>
                            <source>./test/delay_data.txt</source>
                        </plotdata>                    
                        
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
                        
                        <plot>
                            <output>./test/avgDelay.png</output>
                            <title>AvgDelay</title>
                            <data>all_throughtput</data>
                            <index> time </index>
                            <series>  dAvgTh </series>
                            <series> dAvgLat</series>
                            <xlabel> time </xlabel>
                            <ylabel> </ylabel>
                        </plot>
                        
                        <plot>
                            <output>./test/delay_dist.png</output>
                            <title>delay distribution</title>
                            <data>all_delay</data>
                            <index> delay </index>
                            <series>  number </series>
                        </plot>                                                
                    </configure>
                """    
    ELEMENT_LIST = ["datameta","plotdata","plot"]
        
    def __init__(self):
        self.cur_map = None
        self.chars = []
        
        self.datameta = []
        self.plotdata=[]
        self.plot = []
        
        self.meta_map = {"datameta":self.datameta,"plotdata":self.plotdata,"plot":self.plot}
    
    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in PlotMetaHandler.ELEMENT_LIST:
            self.cur_map = {}
        self.chars = []

    def endElement(self, name):
        if name == "configure": return
        if name in PlotMetaHandler.ELEMENT_LIST:
            #print name,self.cur_map
            self.meta_map[name].append(self.cur_map)
        else:
            value = "".join(self.chars).strip()
            #print name,value,self.cur_map
            if self.cur_map.has_key(name):
                self.cur_map[name].append(value)
            else:
                self.cur_map[name] = [value]

    def characters(self, ch):
        self.chars.append(ch) 
    
class PlotMeta(object):
    def __init__(self):
        self.datameta = []
        self.plotdata=[]
        self.plot = []
    
    def loadByFile(self,src):
        handler = PlotMetaHandler()
        xml.sax.parse(src, handler)
    
        self.datameta = handler.datameta
        self.plotdata=handler.plotdata
        self.plot = handler.plot
                
    def loadByStr(self,src):
        handler = PlotMetaHandler()
        xml.sax.parseString(src, handler)
    
        self.datameta = handler.datameta
        self.plotdata=handler.plotdata
        self.plot = handler.plot
    
    def __str__(self):
        data_meta = os.linesep.join([str(x) for x in self.datameta]) 
        plot_meta = os.linesep.join([str(x) for x in self.plotdata])
        plot = os.linesep.join([str(x) for x in self.plot])        
        return os.linesep.join([data_meta,"-"*30,plot_meta,"-"*30,plot])  
    
def testMetaParse():
    dataMeta = PlotMeta()
    dataMeta.loadByStr(PlotMetaHandler.SAMPLE_XML)
    print dataMeta  

if __name__ == '__main__':
    testMetaParse()                  