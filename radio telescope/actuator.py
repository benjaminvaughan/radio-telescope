import math

def function():

    H = 21.5
    theta = 
    xprime = 3 / 5 * H * math.cos(theta)
    fprime = 125
    h1 = 39.5
    hprime = h1 + 3 / 5 * H * math.sin(theta)
    x = 10
    h = 20

    while F != 20:
        
        F = fprime*xprime*math.sin(math.tan(3/5*H*math.cos(theta))) /
        ( x * math.sin( math.tan( x / h)))
        x += .1
        
    print("%f inches" % (x))
    
