function hookjavalangString() {
    Java.perform(function () {
        var JavaString = Java.use('java.lang.String');

        hook_url_encode()
        // hook_string_factory()
        var exampleString1 = JavaString.$new('Hello World, this is an example string in Java.');
        console.log('[+] exampleString1: ' + exampleString1);
    })
}

function hook_url_encode() {
    var v = Java.use('java.net.URLEncoder');
    v.encode.overload('java.lang.String', 'java.lang.String').implementation = function (v1, v2) {
        var v3 = this.encode(v1, v2);
        console.log('encode\t\t', v1, v2, v3);
        return v3
    }
}

//核心加密函数
//搞清楚
function hook_my_sign_h() {
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.h.implementation = function (v1, v2, v3) {
        var v4 = this.h(v1, v2, v3)
        // console.log(v1)
        if (v1.includes('detail')) {
            console.log("加密函数-h-", "v1", v1);
            console.log("加密函数-h-", "v2", v2);
            console.log("加密函数-h-", "v3", v3);
            // console.log("加密函数-h-", "a", this._a.value);
            var HashMap = Java.use('java.util.concurrent.ConcurrentHashMap');
            console.log("局部变量a--" + Java.cast(this._a.value, HashMap).toString());
            var mysign = this.h('https://circle.seeyouyima.com/v5/article_detail?topic_id=69842154&source=1&isloading=0&req_source=0', '5FF9FA2001756C9F8F132863DB583927', requst_data_hashmap)
            console.log(timestamp, uuid);
            console.log('???', mysign);

            console.log('生成', 'https://circle.seeyouyima.com/v5/article_detail?topic_id=69842154&source=1&isloading=0&req_source=0\n&mysign=' + mysign +
                '&timestamp=' + timestamp +
                '&nonce=' + uuid
            )
            console.log("加密函数-h-", "v4", v4);
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
        }
        return v4;
    }

}

function hook_my_sign_e() {
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.e.implementation = function (v1) {
        // console.log("加密函数-e-", "成员变量a", this.a.value);
        var v2 = this.e(v1);
        console.log("加密函数-e-", "v1", v1);
        console.log("加密函数-e-", "v2", v2);
        return v2;
    }
}

function hook_my_sign_b() {
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.b.implementation = function (v1, v2) {
        console.log("加密函数-b-", "v1", v1);
        console.log("加密函数-b-", "v2", v2);
        this.b(v1, v2)
    }
}

function hook_my_sign_f() {
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.f.implementation = function (v1, v2, v3) {
        var v4 = this.f(v1, v2, v3)
        console.log('url==', v1);
        console.log('bool==', v2);
        console.log('url-hash==', "v3", v3);

        var HashMap = Java.use('java.util.HashMap');
        console.log("map：" + Java.cast(v4, HashMap).toString());
        // var sets = v4.entrySet();
        // var iterator = v4.iterator();
        //
        // while (iterator.Next()) {
        //     var val = Java.cast(iterator.next(), Java.use('java.util.Map$Entry'));
        //     console.log(val.getKey(), '---', val.getValue())
        // }
        // // console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
        return v4;
    }
}

function hook_my_sign_i() {
    var prefix = '加密函数-hook_my_sign_i- urlencode--'
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.i.implementation = function (v1, v2) {
        var v3 = this.i(v1, v2)
        console.log(prefix, "v1", v1);
        console.log(prefix, "v2", v2);
        console.log(prefix, "v3", v3);
        return v3;
    }
}

function hook_my_sign_a() {
    var prefix = '加密函数-hook_my_sign_a-'
    var v = Java.use('com.meiyou.framework.ui.http.g');
    v.a.implementation = function (v1) {
        this.a(v1)
        console.log(v1);
    }
}

/*hook string的js方法*/
function hook_string_factory() {
    var StringFactory = Java.use('java.lang.StringFactory');
    StringFactory.newStringFromString.implementation = function (content) {
        console.log("java.lang.StringFactory.newStringFromString->" + content);
        var result = this.newStringFromString(content);
        return result;
    };
}

function show_all_loaded_classes() {
    Java.perform(function () {
        var all_class = Java.enumerateLoadedClassesSync()
        console.log('打印所有的已加载类-', all_class.join('\n'));
    })
}

function dynamic_load_class() {
    Java.enumerateClassLoaders({
        onMatch: function (loader) {
            try {
                Java.ClassFactory.loader = loader;
                var dynamic_class = Java.use('com.meiyou.framework.ui.http.g');
                console.log('动态加载--', dynamic_class);
                hook_my_sign_h();
                // hook_my_sign_e();
                // hook_my_sign_b();
                // hook_my_sign_f();
                // hook_my_sign_i();
                // hook_my_sign_a();
            } catch (e) {
                console.log(e)
            }
        },
        onComplete: function () {
        }
    })
}

function encrypted_test_v1() {
    var String = Java.use("java.lang.String");
    var UUID = Java.use("java.util.UUID");
    // // 获取当前时间戳（秒）
    var timestamp = Math.floor(new Date().getTime() / 1000).toString();
    // // 生成 UUID 并移除短横线
    var uuid = UUID.randomUUID().toString().replace(/-/g, '');
    // 获取 Java 的 HashMap 类
    var HashMap = Java.use("java.util.HashMap");
    var type_string = Java.use("java.lang.String");
    // 创建一个新的 HashMap 实例
    var requst_data_hashmap = HashMap.$new();

    var v = Java.use('com.meiyou.framework.ui.http.g');

    var topic_id = 70000000;
    var init_url = "https://circle.seeyouyima.com/v5/article_detail?topic_id=" + topic_id + "&source=1&isloading=0&req_source=0"
    var api_key = '5FF9FA2001756C9F8F132863DB583927'
    // 向 map 中添加键值对
    requst_data_hashmap.put(type_string.$new('timestamp'), type_string.$new(timestamp));
    requst_data_hashmap.put(type_string.$new('nonce'), type_string.$new(uuid));
    var output_mysign = v.$new().h(init_url, api_key, requst_data_hashmap)

    var output_mysign_v2 = output_mysign.replace(/%/g, '%25')

    console.log(output_mysign, output_mysign_v2)
    console.log('生成链接>>', init_url + '\n&timestamp=' + timestamp + '&nonce=' + uuid + '&mysign=' + output_mysign_v2)
}

function dynamic_load_class_and_hook_encryted_function() {
    Java.enumerateClassLoaders({
        onMatch: function (loader) {
            try {
                Java.ClassFactory.loader = loader;
                var dynamic_class = Java.use('com.meiyou.framework.ui.http.g');
                console.log('动态加载加密函数');
                encrypted_test_v1()
            } catch (e) {
                console.log(e)
            }
        },
        onComplete: function () {
        }
    })
}

function run_demo() {
    Java.perform(function () {
        dynamic_load_class_and_hook_encryted_function()
    })
}


// https://news-node.seeyouyima.com/circle/share.html?topic_id=69842154&_is_share=1&app_id=1&version=&platform=&mysign=06ac9b5e5d5d475e18c6424e0e3a18a94a23d4ad7a9c13a0e554bac268c5d28e
// https://news-node.seeyouyima.com/circle/share.html?topic_id=69842154&_is_share=1&app_id=1&version=&platform=&mysign=06ac9b5e5d5d475e18c6424e0e3a18a94a23d4ad7a9c13a0e554bac268c5d28e