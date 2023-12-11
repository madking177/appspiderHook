# -*- coding: utf-8 -*-
import json
import sys
import frida
import subprocess
from loguru import logger

o1 = subprocess.run('adb forward tcp:27042 tcp:27042', capture_output=True).stdout
logger.info(o1)
o2 = subprocess.run('adb forward tcp:27043 tcp:27043', capture_output=True).stdout
logger.info(o2)

d = frida.get_remote_device()
session = d.attach('com.dragon.read')


def on_msg(msg, data):
    print(msg, data)



script = session.create_script('''
function map_to_json(v) {
    var Gson = Java.use('com.google.gson.Gson').$new();
    return Gson.toJsonTree(v).getAsJsonObject()
}
Java.perform(function () {
    var c1 = Java.use('com.dragon.reader.lib.support.h')//最开始加载到小说的位置
    c1.e.overload('java.lang.String').implementation = function (v1) {
        var v2 = this.e(v1)
        var data = map_to_json(v2)
        console.log('-----', data)
        //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new())) //打印堆栈 方便溯源
        return v2
    }
})
''')

script.on('message', on_msg)
script.load()
sys.stdin.read()
