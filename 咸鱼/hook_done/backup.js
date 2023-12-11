rpc.exports = {

    getsign: function (sign_params) {
        var sign_output = '-1'
        Java.perform(function () {
            var PAGE_ID = 'pageId';
            var PAGE_NAME = 'pageName';
// 定义 HashMap 对象和 String 对象
            var hashMap = Java.use('java.util.HashMap');
            var string = Java.use('java.lang.String');


            function hashPut(hashMap, key, value) {
                if (value === null) {
                    return;
                }
                hashMap.put(string.$new(key), string.$new(value));
            }

// 创建 h1 和 h2 两个 HashMap 对象
            var h1 = hashMap.$new();
            var h2 = hashMap.$new();
            hashPut(h2, PAGE_ID, "");
            hashPut(h2, PAGE_NAME, "");

            var s2 = string.$new();
            var s3 = string.$new('r_115' +
                '');
            console.log("get_sign");
            // 解析sign_params
            var headers_obj = JSON.parse(sign_params);
            // 遍历json对象
            for (var key in headers_obj) {
                console.log(key + " : " + headers_obj[key]);
                hashPut(h1, key, headers_obj[key]);
            }
            var s1 = string.$new(headers_obj['appKey']);

            // 调用 com.taobao.wireless.security.sdk.SecurityGuardManagerImpl.getStaticDataSign 方法
            Java.choose("mtopsdk.security.InnerSignImpl", {
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    var result = instance.getUnifiedSign(h1, h2, s1, s2, false, s3);
                    console.log(result);
                    send({"sign": result.toString()});
                    // 必须返回stop，否则会遍历所有的实例
                    sign_output = result.toString()
                    return "stop";
                },
                onComplete: function () {
                    console.log("Done");
                },
                // 使用 onMatchOnce: true 选项
                onMatchOnce: true
            });
        });

        return JSON.stringify(sign_output)
    },
};

Java.perform(function () {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.p.overload().implementation = function () {
        // console.log('?');
        // console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
        return false;
    }
});
//
// function map_to_json(v) {
//     var Gson = Java.use('com.google.gson.Gson').$new();
//     return Gson.toJsonTree(v).getAsJsonObject()
// }
//
// // hook mtopsdk.mtop.global.SwitchConfig，返回false，禁用spdy协议，可以进行抓包
Java.perform(function () {


    var b = Java.use("mtopsdk.security.InnerSignImpl")
    b.getUnifiedSign.implementation = function (v1, v2, v3, v4, v5, v6) {
        var v7 = this.getUnifiedSign(v1, v2, v3, v4, v5, v6)
        console.log('v1:', v1)
        console.log('v2:', v2)
        console.log('v3:', v3)
        console.log('v4:', v4)
        console.log('v5:', v5)
        console.log('v6:', v6)
        console.log('v7:', v7)
        return v7
    }
    // b.getUnifiedSign
});






