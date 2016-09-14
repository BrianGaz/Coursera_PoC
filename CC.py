"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
from math import ceil
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.total_cookies = 0.0
        self.current_cookies = 0.0
        self.current_time = 0.0
        self.cps = 1.0
        # then keeping a history of the game:
        # a time, an item, the cost of that item, total number by that time
        self.history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return 'Total Cookies: ' + str(self.total_cookies)+ '\n' \
                'Current Cookies: ' + str(self.current_cookies)+ '\n' \
                'Current Time: ' + str(self.current_time) + '\n' \
                'Current CPS: ' + str(self.cps) + '\n' \
                'History: ' + str([i for i in self.history])
                               

        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.current_cookies >= cookies:
            return 0.0
        cookie_diff = cookies - self.current_cookies
        seconds = cookie_diff / self.cps
        return ceil(seconds)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            pass
        self.total_cookies += time * self.cps
        self.current_cookies += time * self.cps
        self.current_time += time
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.current_cookies:
            pass
        self.current_cookies -= cost
        self.cps += additional_cps
        self.history.append((self.current_time, item_name, cost,
                             self.total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_ = build_info.clone()
    clicker_ = ClickerState()
    while clicker_.get_time() <= duration:
        
        buy_name = strategy(clicker_.get_cookies,
                            clicker_.get_cps(),
                            clicker_.get_history(),
                            duration - clicker_.get_time(),
                            build_)
        buy_cost = build_.get_cost(buy_name)
        buy_cps = build_.get_cps(buy_name)
        
        if buy_name == None:
            break
        
        #Time until cookies reaches the point of being able to buy.
        time_until_buy = clicker_.time_until(build_.get_cost(buy_name))
        
        if time_until_buy == 0 and time_until_buy <= duration:
            clicker_.buy_item(buy_name, buy_cost, buy_cps)
            build_.update_item(buy_name)
        else:
            clicker_.wait(time_until_buy)
          
    return clicker_


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    build_ = build_info.clone()
    item_prices = {}
    
    for item in build_.build_items():
        item_prices[item] = build_.get_cost(item)
        
    min_cost = min(item_prices.values())
    
    for item,price in item_prices.items():
        if price == min_cost:
            return item
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    build_ = build_info.clone()
    item_prices = {}
    
    for item in build_.build_items():
        item_prices[item] = build_.get_cost(item)
        
    max_cost = max(item_prices.values())
    
    for item,price in item_prices.items():
        if price == max_cost:
            return item
    return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name,"\n","=====","\n", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
#print strategy_cheap(0, 1, [0,None,0,0], 100, provided.BuildInfo())
