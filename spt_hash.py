
# coding: utf-8
import time
__base32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
__decodemap = { }
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i
del i

def time_coordinate(t, default_midtime="2016-06-01", year_range=4, flags=True):
    def isnumeric(s):
        return type(s) == type(1) or type(s) == type(1.1)

    if not isnumeric(t):
        raise Exception("time param is must be a number or a Object that can be converted to a number")

    pole_st = time.strptime(default_midtime,"%Y-%m-%d")
    midtime=time.mktime(pole_st)
    
    lst = list(pole_st)
    lst[0]=lst[0]-year_range/2
    stime = time.mktime(lst)
    if flags:
        return (t - midtime) *(180.0/(midtime - stime)) #2 years seconds to 180 pice, per pice (5*365*86400)/180
    else:
        return t / (180.0 / (midtime - stime)) + midtime


def encode_spthash_flex(latitude, longitude, time, default_midtime="2016-06-01", year_range=4, precision=30):
    time_coords = time_coordinate(time, default_midtime, year_range)
    return encode_spthash(latitude, longitude, time_coords, precision)

def decode_spthash_flex(code, default_midtime="2016-06-01", year_range=4, precision=30):
    lat, lon, time_coords, lat_err, lon_err, time_err = decode_spthash(code)
    
    time = time_coordinate(time_coords, default_midtime, year_range, False)
    return lat, lon, time, lat_err, lon_err, time_err




def encode_spthash(latitude, longitude, time, precision=30):
    """
    16 char common 90bit infomathion,30 bit is lon, 30 bit is lat
    and 30 bit is time
    """
    lat_interval, lon_interval, time_interval = (-90.0, 90.0), (-180.0, 180.0), (-180.0, 180.0)
    spthash = []
    bits = [ 4, 2, 1 ]
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
        if bit < 2:
            bit += 1
        else:
            spthash += __base32[ch]
            bit = 0
            ch = 0
    return ''.join(spthash)

def decode_spthash(spthash):
    """
    """
    lat_interval, lon_interval,time_interval = (-90.0, 90.0), (-180.0, 180.0), (-180.0, 180.0)
    lat_err, lon_err, time_err = 90.0, 180.0, 180.0
    even = 0
    for c in spthash:
        cd = __decodemap[c]
        for mask in [4, 2, 1]:
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


def clut_spthash_range(arg):
    l = 0
    if isinstance(arg, str) and len(arg) >= 1:
        l = len(spthash)
    elif isinstance(arg, int) and arg >= 1:
        l = arg
    else:
        print "param error"
        return None

    bits = l * 3
    time = lon = lat = bits / 3
    bits = bits % 3
    if bits == 2:
        lon = lon + 1
        lat = lat + 1
    elif bits == 1:
        lon = lon + 1
    #print("lon:" + str(180.0/(2**lon)) + " lat:" + str(360.0/(2**lat)) + " time:" + str(360.0/2**time))
    return {"lon":360.0/(2**lon),"lat":180.0/(2**lat),"time":360.0/(2**time) }
    

def gen_all_range(year_range=10):
    for i in range(31):
		ret = clut_spthash_range(i)
		if ret:
			print("len:"+str(i))
			print("lat:"+str(ret["lat"]) + " distance:"+str(ret["lat"]*111000))
			print("lon:"+str(ret["lon"]) + " distance:"+str(ret["lon"]*111000))
			print("time:"+str(ret["time"]) + " realtime:"+ str(ret["time"]*((year_range*356*86400)/360)))

