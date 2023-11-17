import math

def effal(hcnv, Al_an, Al_lon, Al_al):
    k = 0.0215 #'kW/m-K
    perimetro_base_aleta = 2 * Al_an + 2 * Al_lon
    area_base_aleta = Al_an * Al_lon
    m = (hcnv * perimetro_base_aleta / (k * area_base_aleta)) ** (1/2)
    effal = tanh(m * Al_al) / (m * Al_al)
    return effal

def hcnvi(hcnv, Al_an, Al_lon, Al_al, Arl, Art, Ari):
    hcnvi = (effal(hcnv, Al_an, Al_lon, Al_al) * Art + Arl) * hcnv / Ari
    return hcnvi

def tanh(angulo):
    tanh = (math.exp(angulo)-math.exp(-angulo)) / (math.exp(angulo)+math.exp(-angulo))
    return tanh