from numpy import exp

def gauss(x, pos, amp=1, sigma=1):
    return amp * exp(-(x - pos)**2 / (2*sigma**2))
