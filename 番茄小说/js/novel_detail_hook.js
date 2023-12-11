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
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))

        return v2
    }
})
