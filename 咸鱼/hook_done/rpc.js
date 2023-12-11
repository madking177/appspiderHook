const PAGE_ID = 'pageId';
const PAGE_NAME = 'pageName';
// 定义 HashMap 对象和 String 对象
const hashMap = Java.use('java.util.HashMap');
const string = Java.use('java.lang.String');


function hashPut(hashMap, key, value) {
    if (value === null) {
        return;
    }
    hashMap.put(string.$new(key), string.$new(value));
}

// 创建 h1 和 h2 两个 HashMap 对象
let h1 = hashMap.$new();
let h2 = hashMap.$new();
hashPut(h2, PAGE_ID, "");
hashPut(h2, PAGE_NAME, "");

let s2 = string.$new();
let s3 = string.$new('r_106');



rpc.exports = {
    getsign: function(sign_params) {
        Java.perform(function() {
            console.log("get_sign");
            // 解析sign_params
            let headers_obj = JSON.parse(sign_params);
            // 遍历json对象
            for (let key in headers_obj) {
                console.log(key + " : " + headers_obj[key]);
                hashPut(h1, key, headers_obj[key]);
            }
            let s1 = string.$new(headers_obj['appKey']);
            // 调用 com.taobao.wireless.security.sdk.SecurityGuardManagerImpl.getStaticDataSign 方法
            Java.choose("mtopsdk.security.InnerSignImpl", {
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    var result = instance.getUnifiedSign(h1, h2, s1, s2, false, s3);
                    console.log(result);
                    send({ "sign": result.toString()});
                    // 必须返回stop，否则会遍历所有的实例
                    return "stop";
                },
                onComplete: function () {
                    console.log("Done");
                },
                // 使用 onMatchOnce: true 选项
                onMatchOnce: true
            });
        });
    },
};
// hook mtopsdk.mtop.global.SwitchConfig，返回false，禁用spdy协议，可以进行抓包
Java.perform(function() {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.A.overload().implementation = function () {
        return false;
    }
});


