
# coding: utf-8

__base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
__decodemap = { }
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i
del i

def time_coordinate(t):
    import time
    pole_st = time.strptime("2012-12-21","%Y-%m-%d")
    midtime=time.mktime(pole_st)
    
    lst = list(pole_st)
    lst[0]=lst[0]-5 
    stime = time.mktime(lst)
    return (t - midtime) *(180.0/(midtime - stime))


#import time
#time.time()
#time_coordinate(time.mktime(time.strptime("1992-12-21", "%Y-%m-%d")))

def encode_spthash(latitude, longitude, time, precision=16):
    """
    16 char common 90bit infomathion,30 bit is lon, 30 bit is lat
    and 30 bit is time
    """
    lat_interval, lon_interval, time_interval = (-90.0, 90.0), (-180.0, 180.0), (-180, 180)
    spthash = []
    bits = [ 16, 8, 4, 2, 1 ]
    bit = 0
    ch = 0
    even = 0
    while len(spthash) < precision:
        if even % 3 == 0:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
   
        if even % 3 == 1:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)

        if even % 3 == 2:
            mid = (time_interval[0] + time_interval[1]) / 2
            if time > mid:
                ch |= bits[bit]
                time_interval = (mid, time_interval[1])
            else:
                time_interval = (time_interval[0], mid)

        even = even + 1
        if bit < 4:
            bit += 1
        else:
            spthash += __base32[ch]
            bit = 0
            ch = 0
    return ''.join(spthash)


#encode_day(90,180, time_coordinate(time.mktime(time.strptime("2012-12-21", "%Y-%m-%d"))))
#encode_day(90,180, 180)
#encode_day(-90,-180, -180)
#encode_day(0,0, 0)


def decode_spthash(spthash):
    """
    """
    lat_interval, lon_interval,time_interval = (-90.0, 90.0), (-180.0, 180.0), (-180.0, 180.0)
    lat_err, lon_err, time_err = 90.0, 180.0, 180.0
    even = 0
    for c in spthash:
        cd = __decodemap[c]
        for mask in [16, 8, 4, 2, 1]:
            if even % 3 == 0: # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0]+lon_interval[1])/2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0]+lon_interval[1])/2)
            if even % 3 == 1:      # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0]+lat_interval[1])/2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0]+lat_interval[1])/2)
            if even % 3 == 2:
                time_err /= 2
                if cd & mask:
                    time_interval = ((time_interval[0]+time_interval[1])/2, time_interval[1])
                else:
                    time_interval = (time_interval[0], (time_interval[0]+time_interval[1])/2)
            even = even + 1
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    time = (time_interval[0] + time_interval[1]) / 2
    return lat, lon, time,lat_err, lon_err, time_err


#decode_exactly("zzzzzzzzzzzzzzzz")


def clut_spthash_range(spthash):
    l = len(spthash)
    bits = l * 5
    time = lon = lat = bits / 3
    bits = bits % 3
    if bits == 2:
        lon = lon + 1
        lat = lat + 1
    elif bits == 1:
        lon = lon + 1
    print("lon:" + str(180.0/(2**lon)) + " lat:" + str(360.0/(2**lat)) + " time:" + str(360.0/2**time))
    


#clut_spthash_range("zzzzzzzzzzzzzzzz")

