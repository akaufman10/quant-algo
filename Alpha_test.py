# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:03:30 2017

@author: alex
"""

# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline import CustomFactor
from quantopian.pipeline.factors import VWAP
from quantopian.pipeline.data.builtin import USEquityPricing
import numpy as np   
    

#Alpha#41: (((high * low)^0.5) - vwap) 
class Alpha41(CustomFactor):
    
    inputs = [USEquityPricing.close,
              USEquityPricing.volume,
              USEquityPricing.high,
              USEquityPricing.low]
    
    window_length=1
    
    def compute(self, today, assets, out, close, volume, high, low):
        
        vwap = np.nansum(close * volume, axis=0) / np.nansum(volume, axis=0)
        
        hi_low = (high * low)**.5
        
        out[:] = hi_low - vwap

class CustVwap(CustomFactor):
    
    inputs = [USEquityPricing.close,
              USEquityPricing.volume]
    
    def compute(self, today, assets, out, close, volume):
        out[:] = np.nansum(close * volume, axis=0) / np.nansum(volume, axis=0)    
'''
#paper algo 101 
class a101(CustomFactor):

    inputs = [USEquityPricing.close,
              USEquityPricing.high,
              USEquityPricing.low]
    
    def compute(self, today, assets, out, close, high, low):       
     out[:] = close[-1] 
'''    

def initialize(context):
    pipe = Pipeline()
    pipe = attach_pipeline(pipe, name='test')
    
    one = CustVwap(inputs=[USEquityPricing.close, USEquityPricing.volume], window_length=10)
    
    two = Alpha41(inputs=[USEquityPricing.close,  USEquityPricing.volume, USEquityPricing.high, USEquityPricing.low])
    
    pipe.add(preset, 'one')
    pipe.add(custom, 'two')
    
    #screen = preset.top(500)
    screen2 = custom.top(500)
    
    pipe.set_screen(screen2)
    pass

def before_trading_start(context, data):
    context.output = pipeline_output('test')

    print context.output.head(5)
    update_universe(context.output.index)

# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    
    print context.output.head(5)
    
    #log.info('test')
    # Implement your algorithm logic here.

    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.

    # Place orders with the order(SID, amount) method.

    # TODO: implement your own logic here.
    #order(sid(24), 50)

    
