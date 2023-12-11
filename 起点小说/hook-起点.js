function hook_java_map(include_words) {
    var index = 0
    console.log('include_words\t', include_words)
    var hmap = Java.use("java.util.HashMap");
    // var hmap = Java.use("java.util.HashMap");
    hmap.put.implementation = function (key, val) {
        if (key != null) {
            var keytext = key.toString().toLowerCase()
            if (keytext.includes(include_words)) {
                index += 1
                console.log(index, key)
                console.log('print map\t', java_map_to_string(this))
                // print_call_trace()
            }
        }

        return this.put(key, val)
    }
}

// hook 所有字符串类型
// hook 所有字符串类型
function hook_string_factory() {
    var index = 0;

    var StringFactory = Java.use('java.lang.StringFactory');
    StringFactory.newStringFromString.implementation = function (content) {
        index += 1;
        // console.log(this.$className)
        if (content.includes('道爷要长生')) {
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
        }
        console.log(index, "->" + content);
        var result = this.newStringFromString(content);
        return result;
    };
}

// 打印一个调用堆栈
function print_call_trace() {
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
}

function print_all_methods(classObject) {
    var methods = classObject.class.getDeclaredMethods();
    methods.forEach(function (method) {
        console.log('打印所有函数方法\t', method.getName());
    });
}

// 通过加载器获得类
function find_class_by_class_loader() {
    console.log('-----------------------------------');
    Java.choose("dalvik.system.PathClassLoader", {
        onMatch: function (instance) {
            // console.log(instance)
            // console.log(Java.ClassFactory)
            var factory = Java.ClassFactory.get(instance)
            try {
                var method_name = 'initQDHttp$lambda-1'
                var myClass = factory.use('com.qidian.QDReader.start.AsyncMainQDHttpTask')
                console.log('find it\t=', myClass)
                print_all_methods(myClass)
                try {
                    myClass[method_name].implementation = function (v1, v2, v3) {
                        var v4 = myClass[method_name](v1, v2, v3)

                        console.log('v1\t', v1)
                        console.log('v2\t', v2)
                        console.log('v3\t', v3)
                        if (v3 != null) {
                            print_all_methods(v3)
                        }

                        console.log('v4\t', java_map_to_string(v4))
                        // console.log('?\t', v1, v2, v3, java_map_to_string(v4))
                        print_call_trace()
                        return v4
                    }
                    console.log('hook了调用栈方法\t', myClass.class)
                } catch (e) {
                    console.log(e)
                }
                return "stop"
            } catch (e) {
                // console.log("next")
                // console.error(e)
            }
        }, onComplete: function () {
            console.log("Done")
        }
    })
}

function hook_final() {
    var val = Java.use('com.qidian.QDReader.component.util.FockUtil')
    val.getH.implementation = function (v1, v2, v3) {
        var v4 = this.getH(v1, v2, v3)
        console.log('hook 到header函数\t', v1, v2, v3.toString(), java_map_to_string(v4))
        return v4
    }
}

function hook_java_list() {
    var ArrayList = Java.use('java.util.ArrayList');

    ArrayList.add.overload('java.lang.Object').implementation = function (v1) {
        try {
            if (v1 == null) {
                return this.add(v1)
            }
            var text = (v1 + '').toLowerCase().trim()
            if (text.includes('bookdetail/get') && !text.includes('charles')) {
                console.log(v1)
                print_call_trace()
            }

        } catch (e) {

        }
        return this.add(v1)
    }
    ArrayList.add.overload('int', 'java.lang.Object').implementation = function (v1, v2) {
        try {
            var text = (v2 + '').toLowerCase().trim()
            if (text.includes('bookdetail/get') && !text.includes('charles')) {
                console.log(v2)
            }

        } catch (e) {

        }
        // console.log(v1, v2)
        this.add(v1, v2)
    }

    // .implementation = function (index, obj) {
    //     // 在这里添加你的逻辑，可以打印参数、修改参数等
    //     console.log('ArrayList.add() called with index:', index, 'and object:', obj);
    //
    //     // 调用原始的 ArrayList.add() 方法
    //     return this.add(index, obj);
    // };
}

function java_map_to_string(v1) {
    return Java.cast(v1, Java.use('java.util.HashMap')).toString()
}


// 通过加载器获得类
function find_class_by_class_loader_v2() {
    console.log('-----------------------------------');
    Java.choose("dalvik.system.PathClassLoader", {
        onMatch: function (instance) {
            // console.log(instance)
            // console.log(Java.ClassFactory)
            var factory = Java.ClassFactory.get(instance)
            try {
                var method_name = 'initQDHttp$lambda-2'
                var myClass = factory.use('com.qidian.QDReader.start.AsyncMainQDHttpTask')
                console.log('find it\t=', myClass)
                print_all_methods(myClass)
                try {
                    myClass[method_name].implementation = function (v1) {
                        console.log(v1)
                        myClass[method_name]()
                    }
                    console.log('hook了调用栈方法\t', myClass.class)
                } catch (e) {
                    console.log(e)
                }
                return "stop"
            } catch (e) {
                // console.log("next")
                // console.error(e)
            }
        }, onComplete: function () {
            console.log("Done")
        }
    })
}

var proceed_index = 0

function java_hook_proceed_chain(className) {
    //hook调用链
    proceed_index += 1
    var function_call_index = proceed_index
    var myclass = Java.use(className)

    myclass.intercept.implementation = function (request) {
        console.log('request\t', request.request())
        // console.log('request header\t', request.request().headers())

        var response = this.intercept(request)

        // console.log('request header2\t', request.request().headers())


        // console.log('\nresponse=', v2.toString())
        // if (response.toString().includes('v3/bookdetail/get')) {
        if (response.toString().includes('')) {
            // console.log(function_call_index, '---------------------------------')
            // console.log(className + '\nheaders=', v1.request().headers())
            // console.log(v1, v2)
            // print_call_trace()

            // console.log('response\t', response)
        }
        // console.log('触发调用链response\t', v2)

        return response
    }
}

function map_to_json(v) {
    var Gson = Java.use('com.google.gson.Gson').$new();
    return Gson.toJsonTree(v).getAsJsonObject()
}

function hook_headers() {
    var native_class = Java.use('com.qidian.QDReader.component.util.FockUtil')
    native_class.addRetrofitH.implementation = function (v1) {
        var v2 = this.addRetrofitH(v1)
        if (v1 != null) {
            console.log('?1', v1.class, v1.headers(), '\t', v1.toString())
            header_demo()
            if (v1.tags != null) {
                console.log('?1.1', v1.tags.value)
                // console.log('?1.1', v1.tags.value)
            } else {
                console.log('?1.1')
            }
            console.log('?2', v1.class, v2.headers())
        }

        return v2
    }

    return;
    // hook request
    var req = Java.use('okhttp3.Request$Builder')
    print_all_methods(req)
    req.addHeader.implementation = function (v1, v2) {

        if (v1.toString().includes('borgus')) {
            console.log(v1, v2)
            print_call_trace()
        }
        // console.log(v1)
        // this.Requst()
        var v3 = this.addHeader(v1, v2)
        // console.log(v1, v2)
        return v3
    }
    return

    // hook headers
    var myclass = Java.use('okhttp3.Headers')
    myclass['of'].overload('java.util.Map').implementation = function (v1) {
        var v2 = this.of(v1)
        console.log('?1', Java.cast(v1, Java.use('java.util.HashMap')))
        return v2;
    }
    myclass['of'].overload('[Ljava.lang.String;').implementation = function (v1) {
        var v2 = this.of(v1)
        console.log('?2', v1.toString())
        return v2;
    }
}


function header_demo(book_id) {
    var native_class = Java.use('com.qidian.QDReader.component.util.FockUtil')
    var okhttp_client = Java.use('okhttp3.OkHttpClient').$new()
    var request_class = Java.use('okhttp3.Request')
    var class_builder = Java.use('okhttp3.Request$Builder')
    var class_string = Java.use("java.lang.String");

    console.log('------------------------------------')
    var new_builder = class_builder.$new().url(class_string.$new('https://druidv6.if.qidian.com/argus/api/v3/bookdetail/get?bookId=103' + book_id + '&isOutBook=0')).method(class_string.$new('GET'), null)

    var new_request = request_class.$new(new_builder)
    // console.log(native_class.class)
    // print_all_methods(native_class)
    var native_instance = native_class.$new()
    // var native_instance = native_class.INSTANCE
    // console.log('?', native_instance.class)
    var new_request_by_so = native_instance.addRetrofitH(new_request)

    console.log('?api\t', new_request_by_so.headers())

    var response = okhttp_client.newCall(new_request_by_so).execute()

    // console.log(response)
    console.log(response.body().string())

    console.log('book-id\t103', book_id,)
    // print_all_methods(response.body())
    // var source = response.body().source()
    //
    // source.request(100000000)
    //
    // var clone = source.buffer().clone()
    //
    // var charset = Java.use('java.nio.charset.Charset').forName('UTF-8')
    //
    //
    // console.log('?clone\t', clone.class)
    // var text = clone.readString()
    // console.log(text)
}


Java.perform(function () {

    // hook_java_map('qdsign')
    // return;
    // hook_final()
    // return
    /*hook string的js方法*/
    // find_class_by_class_loader()
    // hook_java_list()

    // find_class_by_class_loader_v2()

    //hook调用链 可以打印出所有请求
    // java_hook_proceed_chain('com.qidian.QDReader.framework.network.retrofit.c')
    // java_hook_proceed_chain('com.qidian.QDReader.component.retrofit.c')
    // java_hook_proceed_chain('com.qidian.QDReader.component.retrofit.d')
    // java_hook_proceed_chain('com.qidian.QDReader.framework.network.common.cihai')
    // hook_headers()

    header_demo(7750279)
})



