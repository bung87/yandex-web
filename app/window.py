from functools import partial

_methods = ('assert,clear,count,debug,dir,dirxml,error,exception,group,' +
     'groupCollapsed,groupEnd,info,log,markTimeline,profile,profiles,profileEnd,' +
     'show,table,time,timeEnd,timeline,timelineEnd,timeStamp,trace,warn').split(',')

class Console:

    def __init__(self,webdriver):
        self.webdriver = webdriver

    def _base(self,method,*args):
        pass
        # self.webdriver.execute_script('console.%s.apply(null,Array.prototype.slice.apply(arguments))' % method,*args)

    def __getattr__(self, name):
        return partial(Console._base,self,name)
