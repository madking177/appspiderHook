import frida
import time
import ctypes
import hashlib
import random
import uuid
import time
import gzip
import requests
from urllib.parse import quote_plus
from urllib.parse import urlencode

SCRIPT = None


def md5(data_string):
    obj = hashlib.md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def create_random_mac(sep=":"):
    """ 随机生成mac地址 """

    def mac_same_char(mac_string):
        v0 = mac_string[0]
        index = 1
        while index < len(mac_string):
            if v0 != mac_string[index]:
                return False
            index += 1
        return True

    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)

    if not mac_same_char(mac) and mac != "00:90:4C:11:22:33":
        return mac

    return create_random_mac(sep)


def create_cdid():
    return str(uuid.uuid4())


def create_openudid():
    return "".join([hex(i)[2:] for i in random.randbytes(10)])


def m44417a(barr):
    def int_overflow(val):
        maxint = 2147483647
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    def unsigned_right_shift(n, i):
        # 数字小于0，则转为32位无符号uint     n>>>i
        if n < 0:
            n = ctypes.c_uint32(n).value
        # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
        if i < 0:
            return -int_overflow(n << abs(i))
        # print(n)
        return int_overflow(n >> i)

    char_array = "0123456789abcdef"
    result = ['' for i in range(len(barr) * 2)]
    for i in range(len(barr)):
        i2 = barr[i] & 255
        i3 = i * 2
        result[i3] = char_array[unsigned_right_shift(i2, 4)]  # i2>>>4
        result[i3 + 1] = char_array[i2 & 15]
    return ''.join(result)


def get_frida_rpc_script():
    global SCRIPT
    if SCRIPT:
        return SCRIPT

    rdev = frida.get_remote_device()
    session = rdev.attach("com.ss.android.ugc.aweme")

    scr = """
    rpc.exports = {   
        ttencrypt:function(bArr,len){
             var res;

             Java.perform(function () {
                var EncryptorUtil = Java.use("com.bytedance.frameworks.encryptor.EncryptorUtil");  

                // 将bArr转换成Java的字节数组。
                var dataByteArray = Java.array('byte',bArr);

                // 调用native方法，并获取返回值。
                res = EncryptorUtil.ttEncrypt(dataByteArray,len);
             });

             return res;
        },
        execandleviathan: function (i2,str){
            var result;
            Java.perform(function () {
                // 先处理拼接好的数据（字节数组）
                var bArr = [];
                for(var i=0;i<str.length;i+=2){
                    var item = (parseInt(str[i],16) << 4) + parseInt(str[i+1],16);
                    bArr.push(item);
                }

                // 转换为java的字节数组
                var dataByteArray = Java.array('byte',bArr);

                // 调用leviathan方法
                var Gorgon = Java.use("com.ss.sys.ces.a");
                result = Gorgon.leviathan(-1, i2 , dataByteArray);   //leviathan为方法名
            });
            return result;
        }
    }
    """
    script = session.create_script(scr)
    script.load()
    SCRIPT = script
    return script


def get_gorgon(script, param_string, cookie_string, body=None):
    x_ss_stud = None
    if body:
        # 6.对请求体md5加密，生成 x_ss_stud
        ha = hashlib.md5()
        ha.update(bytes(body))
        x_ss_stud = ha.hexdigest().upper()

    # 7.变量a，对URL参数进行md5加密，生成 a
    ha = hashlib.md5()
    ha.update(param_string.encode('utf-8'))
    a = ha.hexdigest()

    # 8.变量str7（get请求时是000.。，post请求时是x_ss_stud ）
    if x_ss_stud:
        str7 = x_ss_stud
    else:
        str7 = '00000000000000000000000000000000'

    # 9.变量str8，对cookie的md5加密（抓包注册设备时cookie是空的；获取评论时cookie才有值）
    if cookie_string:
        str8 = md5(cookie_string)  # 00000000000000000000000000000000 也可以，说明cookie不是必须的。
    else:
        str8 = "00000000000000000000000000000000"

    # 10.变量str9，sessionid的md5（无）
    str9 = "00000000000000000000000000000000"

    # 11.拼接变量
    un_sign_string = "{}{}{}{}".format(a, str7, str8, str9)

    # 12.m44418a处理 + 执行so中的leviathan
    khronos = int(time.time())
    gorgon_byte_list = script.exports.execandleviathan(khronos, un_sign_string)

    # 13.m44417a处理
    gorgon = m44417a(gorgon_byte_list)
    return x_ss_stud, gorgon, khronos


def register_device_encrypt():
    """ 密文注册设备 """
    script = get_frida_rpc_script()

    # 1.生成参数
    mac_addr = create_random_mac()
    cdid = create_cdid()
    clientudid = create_cdid()
    openudid = create_openudid()
    _rticket = int(time.time() * 1000)
    ts = int(time.time())

    # 2.构造请求头和URL参数
    body_tpl = '{"magic_tag":"ss_app_log","header":{"display_name":"抖音短视频","update_version_code":1800,"manifest_version_code":180,"aid":1128,"channel":"sem_shenma_dy_and17","appkey":"57bfa27c67e58e7d920028d3","package":"com.ss.android.ugc.aweme","app_version":"1.8.0","version_code":180,"sdk_version":201,"os":"Android","os_version":"10","os_api":29,"device_model":"Redmi 8A","device_brand":"Xiaomi","device_manufacturer":"Xiaomi","cpu_abi":"armeabi-v7a","build_serial":"unknown","release_build":"024a06f_20200618","density_dpi":320,"display_density":"xhdpi","resolution":"1369x720","language":"zh","mc":"%s","timezone":8,"access":"wifi","not_request_sender":0,"carrier":"中国联通","mcc_mnc":"46001","rom":"MIUI-V12.0.3.0.QCPCNXM","rom_version":"miui_V12_V12.0.3.0.QCPCNXM","sig_hash":"aea615ab910015038f73c47e45d21466","openudid":"%s","clientudid":"%s","serial_number":"unknown","sim_serial_number":[],"region":"CN","tz_name":"Asia\/Shanghai","tz_offset":28800000,"sim_region":"cn"},"_gen_time":%s}'
    body = body_tpl % (mac_addr, openudid, clientudid, _rticket)

    param_string_tpl = "ac=wifi&channel=sem_shenma_dy_and17&aid=1128&app_name=aweme&version_code=180&version_name=1.8.0&device_platform=android&ssmix=a&device_type=Redmi+8A&device_brand=Xiaomi&language=zh&os_api=29&os_version=10&openudid={openudid}&manifest_version_code=180&resolution=720*1369&dpi=320&update_version_code=1800&_rticket={_rticket}&iid=&tt_data=a"
    param_string = param_string_tpl.format(openudid=openudid, _rticket=_rticket)

    # 3.gzip压缩
    gzip_body = gzip.compress(body.encode('utf-8'))
    java_gzip_body = bytearray(gzip_body)
    java_gzip_body[3:10] = [0, 0, 0, 0, 0, 0, 0]

    # 4.执行so请求体加密（ttencrypt）
    ttencrypt_bytes_list = script.exports.ttencrypt(list(java_gzip_body), len(java_gzip_body))

    # 5.字节中的负值的处理（java的字节有符号，python字节无符号），因为后续要进行md5加密，必须是python的字节）
    ttencrypt_to_python_bytes = bytearray([i + 256 if i < 0 else i for i in ttencrypt_bytes_list])

    # 6.对请求体md5加密，生成 x_ss_stud
    ha = hashlib.md5()
    ha.update(bytes(ttencrypt_to_python_bytes))
    x_ss_stud = ha.hexdigest().upper()

    # 7.变量a，对URL参数进行md5加密，生成 a
    ha = hashlib.md5()
    ha.update(param_string.encode('utf-8'))
    a = ha.hexdigest()

    # 8.变量str7（get请求时是000.。，post请求时是x_ss_stud ）
    str7 = x_ss_stud

    # 9.变量str8，对cookie的md5加密（抓包注册设备时cookie是空的；获取评论时cookie才有值）
    str8 = "00000000000000000000000000000000"

    # 10.变量str9，sessionid的md5（无）
    str9 = "00000000000000000000000000000000"

    # 11.拼接变量
    un_sign_string = "{}{}{}{}".format(a, str7, str8, str9)

    # 12.m44418a处理 + 执行so中的leviathan
    khronos = int(time.time())
    gorgon_byte_list = script.exports.execandleviathan(khronos, un_sign_string)

    # 13.m44417a处理
    gorgon = m44417a(gorgon_byte_list)

    # 此时已生成 khronos 和 gorgon

    # 14.发送请求注册设备请求
    res = requests.post(
        url="https://ib.snssdk.com/service/2/device_register/?{}".format(param_string),
        data=ttencrypt_to_python_bytes,
        headers={
            "x-ss-stub": x_ss_stud,
            "content-encoding": "gzip",
            "x-ss-req-ticket": str(khronos),
            "x-khronos": str(khronos),
            "x-gorgon": gorgon,
            "content-type": "application/octet-stream;tt-data=a",
            "user-agent": "okhttp/3.10.0.1"
        }
    )
    device_dict = res.json()
    print(device_dict)
    print('------')
    cookie_dict = res.cookies.get_dict()

    return (
        device_dict,
        cookie_dict,
        {
            'mac_addr': mac_addr,
            'cdid': cdid,
            'clientudid': clientudid,
            'openudid': openudid
        }
    )


def register_device():
    """ 明文注册设备 """
    script = get_frida_rpc_script()

    # 1.生成参数
    mac_addr = create_random_mac()
    cdid = create_cdid()
    clientudid = create_cdid()
    openudid = create_openudid()
    _rticket = int(time.time() * 1000)
    ts = int(time.time())

    # 2.构造请求头和URL参数
    body_tpl = '{"magic_tag":"ss_app_log","header":{"display_name":"抖音短视频","update_version_code":11509900,"manifest_version_code":110501,"app_version_minor":"","aid":1128,"channel":"gdt_growth14_big_yybwz","appkey":"57bfa27c67e58e7d920028d3","package":"com.ss.android.ugc.aweme","app_version":"11.5.0","version_code":110500,"sdk_version":"2.14.0-alpha.4","sdk_target_version":29,"git_hash":"c1aa4085","os":"Android","os_version":"10","os_api":29,"device_model":"Redmi 8A","device_brand":"Xiaomi","device_manufacturer":"Xiaomi","cpu_abi":"armeabi-v7a","release_build":"b44f245_20200615_436d6cbc-aecc-11ea-bfa1-02420a000026","density_dpi":320,"display_density":"xhdpi","resolution":"1369x720","language":"zh","mc":"%s","timezone":8,"access":"wifi","not_request_sender":0,"carrier":"中国联通","mcc_mnc":"46001","rom":"MIUI-V12.0.3.0.QCPCNXM","rom_version":"miui_V12_V12.0.3.0.QCPCNXM","cdid":"%s","sig_hash":"aea615ab910015038f73c47e45d21466","openudid":"%s","clientudid":"%s","sim_serial_number":[],"region":"CN","tz_name":"Asia\/Shanghai","tz_offset":28800,"sim_region":"cn","oaid":{"req_id":"f0959dbb-1be0-4e11-b020-edde265e4aa1","hw_id_version_code":"null","take_ms":"95","is_track_limited":"null","query_times":"1","id":"","time":"1633765787228"},"oaid_may_support":true,"req_id":"8f29815c-a81e-48d0-843b-7c3d17d4f6ef","custom":{"filter_warn":0},"apk_first_install_time":1633765712501,"is_system_app":0,"sdk_flavor":"china"},"_gen_time":%d}'
    body = body_tpl % (mac_addr, cdid, openudid, clientudid, _rticket)

    # param_string_tpl = "ac=wifi&channel=sem_shenma_dy_and17&aid=1128&app_name=aweme&version_code=180&version_name=1.8.0&device_platform=android&ssmix=a&device_type=Redmi+8A&device_brand=Xiaomi&language=zh&os_api=29&os_version=10&openudid={openudid}&manifest_version_code=180&resolution=720*1369&dpi=320&update_version_code=1800&_rticket={_rticket}&iid=&tt_data=a"
    # param_string = param_string_tpl.format(openudid=openudid, _rticket=_rticket)
    param_string_tpl = "ac=wifi&mac_address={mac_addr}&channel=gdt_growth14_big_yybwz&aid=1128&app_name=aweme&version_code=110500&version_name=11.5.0&device_platform=android&ssmix=a&device_type=Redmi+8A&device_brand=Xiaomi&language=zh&os_api=29&os_version=10&openudid={openudid}&manifest_version_code=110501&resolution=720*1369&dpi=320&update_version_code=11509900&_rticket={_rticket}&mcc_mnc=46001&cpu_support64=false&host_abi=armeabi-v7a&app_type=normal&ts={ts}&cdid={cdid}&oaid&manifest_version_code=110501&_rticket={_rticket}&app_type=normal&channel=gdt_growth14_big_yybwz&device_type=Redmi%208A&language=zh&cpu_support64=false&host_abi=armeabi-v7a&resolution=720*1369&openudid=2348574b5d8a004d&update_version_code=11509900&cdid={cdid}&os_api=29&mac_address={mac_addr}&dpi=320&oaid=&ac=wifi&mcc_mnc=46001&os_version=10&version_code=110500&app_name=aweme&version_name=11.5.0&device_brand=Xiaomi&ssmix=a&device_platform=android&aid=1128&ts={ts}"
    param_string = param_string_tpl.format(
        mac_addr=quote_plus(mac_addr),
        openudid=openudid,
        _rticket=_rticket,
        ts=ts,
        cdid=cdid,
    )

    # 3.gzip压缩
    gzip_body = gzip.compress(body.encode('utf-8'))
    java_gzip_body = bytearray(gzip_body)
    java_gzip_body[3:10] = [0, 0, 0, 0, 0, 0, 0]

    # 4.执行so请求体加密（ttencrypt）
    # ttencrypt_bytes_list = script.exports.ttencrypt(list(java_gzip_body), len(java_gzip_body))

    # 5.字节中的负值的处理（java的字节有符号，python字节无符号），因为后续要进行md5加密，必须是python的字节）
    # ttencrypt_to_python_bytes = bytearray([i + 256 if i < 0 else i for i in ttencrypt_bytes_list])

    # 6.对请求体md5加密，生成 x_ss_stud
    ha = hashlib.md5()
    ha.update(bytes(java_gzip_body))
    x_ss_stud = ha.hexdigest().upper()

    # 7.变量a，对URL参数进行md5加密，生成 a
    ha = hashlib.md5()
    ha.update(param_string.encode('utf-8'))
    a = ha.hexdigest()

    # 8.变量str7（get请求时是000.。，post请求时是x_ss_stud ）
    str7 = x_ss_stud

    # 9.变量str8，对cookie的md5加密（抓包注册设备时cookie是空的；获取评论时cookie才有值）
    str8 = "00000000000000000000000000000000"

    # 10.变量str9，sessionid的md5（无）
    str9 = "00000000000000000000000000000000"

    # 11.拼接变量
    un_sign_string = "{}{}{}{}".format(a, str7, str8, str9)

    # 12.m44418a处理 + 执行so中的leviathan
    khronos = int(time.time())
    gorgon_byte_list = script.exports.execandleviathan(khronos, un_sign_string)

    # 13.m44417a处理
    gorgon = m44417a(gorgon_byte_list)

    # 此时已生成 khronos 和 gorgon

    # 14.发送请求注册设备请求

    res = requests.post(
        url="https://ib.snssdk.com/service/2/device_register/?{}".format(param_string),
        data=java_gzip_body,
        headers={
            "x-ss-stub": x_ss_stud,
            "content-encoding": "gzip",
            "x-ss-req-ticket": str(khronos),
            "x-khronos": str(khronos),
            "x-gorgon": gorgon,
            "content-type": "application/json; charset=utf-8",
            "user-agent": "okhttp/3.10.0.1"
        }
    )
    device_dict = res.json()
    print(device_dict)
    print('------')
    cookie_dict = res.cookies.get_dict()

    return (
        device_dict,
        cookie_dict,
        {
            'mac_addr': mac_addr,
            'cdid': cdid,
            'clientudid': clientudid,
            'openudid': openudid
        }
    )


def get_comment_list():
    """ 获取评论 """
    script = get_frida_rpc_script()
    ctime = time.time()

    device_dict, cookie_dict, device_info_dict = register_device_encrypt()
    # device_dict, cookie_dict, device_info_dict = register_device()

    print(device_dict)
    print(cookie_dict)
    print(device_info_dict)

    device_id = device_dict['device_id_str']  # "1891579430189188"  # 必须 且 不能修改
    iid = device_dict['install_id_str']  # "1082357444254472"  # 必须 且 不能修改

    cdid = device_info_dict['cdid']  # "603dd68a-988a-4b04-9204-e47f0792668b"
    openudid = device_info_dict['openudid']  # "2348574b5d8a004d"
    mac_addr = device_info_dict['mac_addr']  # "E0%3A1F%3A88%3AAA%3AB3%3A39"

    # 在获取评论时，没啥用；可以删除 & 可以是空 & 可以是其他值
    ttreq = cookie_dict['ttreq']
    odin_tt = "2e00d7ebb44285f3b13eb73c3e487a05df718ef6f133a7fd9d41287cbe636389685d223452118eb257fa7a328e48a4d119cef4c410ce2c89f03956f5bd95e650"

    param_dict = {
        "aweme_id": "7015444979988319502",
        "cursor": "0",
        "count": "20",
        "address_book_access": "2",
        "gps_access": "2",
        "forward_page_type": "1",
        "channel_id": "0",
        "city": "130400",
        "hotsoon_filtered_count": "0",
        "hotsoon_has_more": "0",
        "follower_count": "0",
        "is_familiar": "0",
        "page_source": "0",
        "manifest_version_code": "110501",
        "_rticket": int(ctime * 1000),
        "app_type": "normal",
        "iid": iid,
        "channel": "gdt_growth14_big_yybwz",
        "device_type": "Redmi%208A",
        "language": "zh",
        "cpu_support64": "false",
        "host_abi": "armeabi-v7a",
        "resolution": "720*1369",
        "openudid": openudid,
        "update_version_code": "11509900",
        "cdid": cdid,
        "os_api": "29",
        "mac_address": mac_addr,
        "dpi": "320",
        "oaid": "",
        "ac": "wifi",
        "device_id": device_id,
        "mcc_mnc": "46001",
        "os_version": "10",
        "version_code": "110500",
        "app_name": "aweme",
        "version_name": "11.5.0",
        "device_brand": "Xiaomi",
        "ssmix": "a",
        "device_platform": "android",
        "aid": "1128",
        "ts": int(ctime)
    }

    param_string = urlencode(param_dict)

    cookie_string = "install_id={}; ttreq={}; odin_tt={}".format(iid, ttreq, odin_tt)

    x_ss_stud, gorgon, khronos = get_gorgon(script, param_string, cookie_string)

    res = requests.get(
        url="https://api3-normal-c-lf.amemv.com/aweme/v2/comment/list/",
        params=param_dict,
        headers={
            "user-agent": "com.ss.android.ugc.aweme/110501 (Linux; U; Android 10; zh_CN; Redmi 8A; Build/QKQ1.191014.001; Cronet/TTNetVersion:3c28619c 2020-05-19 QuicVersion:0144d358 2020-03-24)",
            "x-khronos": str(khronos),
            "x-gorgon": gorgon
        },
        cookies={
            "install_id": iid,
            "ttreq": ttreq,
            "odin_tt": odin_tt
        }
    )

    print("\n\n\n -------获取评论------- \n\n")
    print(res.text)


if __name__ == '__main__':
    get_comment_list()

