
def geometric_rate(r, n):
    return ((1 + r) ** (1 / n)) - 1


# what is the effective rate r if the subrate is d?
# e.g. if d is the daily growth rate, what is the 30-day rate r?
def effective_rate(d, n):
    return ((1 + d) ** n) - 1


# given a periodic rate of r, a principal of p, and number of periods n, what is the ending principal?
def func_ending_principal(p, r, n):
    return p*((1 + r) ** n)
