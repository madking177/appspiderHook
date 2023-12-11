
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