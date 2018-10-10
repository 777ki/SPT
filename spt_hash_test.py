from spt_hash import *
import random
import time

import pdb
#pdb.set_trace()
def test(lat, lon, tm):
    print("===============TEST=================")
    code = encode_spthash(lat, lon, tm)
    print("[lat:%f, lon:%f, time:%f] => { code:%s } " %(lat, lon, tm, code))
    lat,lon,time,lat_err,lon_err,time_err = decode_spthash(code)
    print("[code:%s] => { lat:%.15f, lon:%.15f, time:%.15f, lat_err:%.15f, on_err:%.15f, time_err:%.15f" %(code, lat, lon, time, lat_err, lon_err, time_err))
    print("===============END==================")

test(37.46874584, 93.23423423, 1000)
test(90, 180, 1000)
test(90,-180, 1000)
test(-90,180, -20)
test(-90,-180, 300)
test(0,0, 1000)
test(0,180, 1000)
test(0,-180, 1000)
test(90,0, 1000)
test(90,-180, 11.5)
test(90,180, 0)
test(90,180, 360)
test(90,180, -360)

def auto_test():
    for i in range(300):
        lat = random.randint(-89, 89) + random.random() * (-1)** random.randint(0,1)
        lon = random.randint(-179, 179) + random.random() * (-1)** random.randint(0,1)
        t = int(time.time()) + random.randint(1, 1000000) *(-1)** random.randint(0,1)
        print("===============TEST=================")
        print(lat, lon, t)
        code=encode_spthash_flex(lat, lon, t)
        print code
        print decode_spthash_flex(code)

auto_test()

code=encode_spthash_flex(23.023, 132.2344, 1496811929)
print code
print decode_spthash_flex(code)
code=encode_spthash_flex(23.023, 132.2344, 1496811929, "2017-06-01")
print code
print decode_spthash_flex(code, "2017-06-01")
code=encode_spthash_flex(23.023, 132.2344, 1496811929, "2018-06-01")
print code
print decode_spthash_flex(code, "2018-06-01")

print("==")
code=encode_spthash_flex(30.23521, 120.17463, time.mktime(time.strptime("20161003021000", "%Y%m%d%H%M%S")), "2014-12-01", 12, 12)
print code
print decode_spthash_flex(code, "2014-12-01")

code=encode_spthash_flex(30.23881, 120.18866, time.mktime(time.strptime("20160414120400", "%Y%m%d%H%M%S")), "2014-12-01", 12, 12)
print code
print decode_spthash_flex(code, "2014-12-01")


print("==")
code=encode_spthash_flex(120.17463,30.23521,  time.mktime(time.strptime("20161003021000", "%Y%m%d%H%M%S")), "2014-12-01")
print code
print decode_spthash_flex(code, "2014-12-01")

code=encode_spthash_flex(120.18866,30.23881,  time.mktime(time.strptime("20160414120400", "%Y%m%d%H%M%S")), "2014-12-01")
print code
print decode_spthash_flex(code, "2014-12-01")

#gen_all_range()
