function map_to_json(v) {
    var Gson = Java.use('com.google.gson.Gson').$new();
    return Gson.toJsonTree(v).getAsJsonObject()
}

//
//
// Java.perform(function () {
//     var a = Java.use('android.widget.TextView')//最开始加载到小说的位置
//     a.setText.overload('java.lang.CharSequence').implementation=function (text) {
//         this.setText(text)
//         console.log(text)
//         console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))
//     }
// })
// Java.perform(function () {
//     var a = Java.use("java.util.HashMap");
//     a.put.implementations = function (a, b) {
//         console.log(a, b);
//         this.put(a, b);
//     }
// });


Java.perform(function () {
    var a = Java.use("java.util.ArrayList");
    a.add.implementations = function (a, b) {
        this.add(a)
    }
});

