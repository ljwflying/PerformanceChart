'''
Created on 2011-7-6

@author: terry
'''
import xml.sax
from xml.sax.handler import ContentHandler
import os

class ColumnDesc(object):
    def __init__(self,index=None,name=None,unit=""):
        self.index = index
        self.name = name
        self.unit = unit
        if not self.unit:
            self.unit = ""
    
    def __str__(self):
        return "[ColumnDesc: index=%2d, name=%s, unit=%s]"%(self.index,self.name,self.unit)

class DataMetaHandler(ContentHandler):
    """parse data meta"""
    
    SAMPLE_XML = """<?xml version="1.0" encoding="utf-8"?>
                    <configure>
                    <entry>
                        <index>0</index>
                        <name>time</name>
                        <unit>second</unit>
                    </entry>
                    <entry>
                        <index>1</index>
                        <name>throughtput</name>
                        <unit>ops/sec</unit>
                    </entry>
                    </configure>
                """
    
    ENTRY = "entry"
    INDEX = "index"
    NAME = "name"
    UNIT = "unit"
    START = "configure"
    
    ELEMENT_LIST = [ENTRY,INDEX,NAME,UNIT,START,]
        
    def __init__(self):
        self.cur_entry = None
        self.chars = []
        self.entries = {}
    
    @staticmethod
    def _parse_entry(item):
        if item.entries.has_key(item.cur_entry.index):
            raise Exception("Duplicate ColumnDesc: cur %s vs old %s"%(item.cur_entry,item.entries[item.cur_entry.index]))
        item.entries[item.cur_entry.index] = item.cur_entry
    
    @staticmethod
    def _parse_index(item):
        item.cur_entry.index =  int("".join(item.chars).strip())
    
    @staticmethod
    def _parse_name(item):
        item.cur_entry.name = "".join(item.chars).strip()
    
    @staticmethod
    def _parse_unit(item):
        item.cur_entry.unit = "".join(item.chars).strip() 
    
    @staticmethod
    def _parse_other(item):
        pass
    
    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        if name not in DataMetaHandler.ELEMENT_LIST:
            raise Exception("unexpected element "+name)
        self.chars = []
        
        if name == DataMetaHandler.ENTRY:
            self.cur_entry = ColumnDesc()
            return

    def endElement(self, name):
        #print name,dir(DataMetaHandler)
        getattr(self,"_parse_"+name,DataMetaHandler._parse_other)(self)

    def characters(self, ch):
        self.chars.append(ch) 



class DataMeta(object):
    def __init__(self):
        self.index_map = {}
        self.name_map = {}
    
    def loadByFile(self,src):
        handler = DataMetaHandler()
        xml.sax.parse(src, handler)
    
        for k,v in handler.entries.items():
            self.index_map[k] = v
            self.name_map[v.name] = v
                
    def loadByStr(self,src):
        handler = DataMetaHandler()
        xml.sax.parseString(src, handler)
    
        for k,v in handler.entries.items():
            self.index_map[k] = v
            self.name_map[v.name] = v
    
    def getByIndex(self,index):
        return self.index_map.get(index,None)

    def getByName(self,name):
        return self.name_map.get(name,None)
    
    def __str__(self):
        return os.linesep.join([str(x) for x in self.index_map.values()])
  
def testMetaParse():
    dataMeta = DataMeta()
    dataMeta.loadByStr(DataMetaHandler.SAMPLE_XML)
    print dataMeta  

if __name__ == '__main__':
    testMetaParse()