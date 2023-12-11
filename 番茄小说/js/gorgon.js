function print() {
    console.log(JSON.stringify(arguments))
}

rpc.exports = {
    gorgonStr128: function (v1, time, str128) {
        var data;
        Java.perform(function () {
            var v3 = []
            for (var index = 0; index < str128.length; index += 2) {
                var number = (parseInt(str128[index], 16) << 4) + parseInt(str128[index + 1], 16)
                v3.push(number)
            }
            v3 = Java.array('byte', v3)
            var gorgon_class = Java.use('com.ss.sys.ces.a')
            var token = gorgon_class.leviathan(v1, time, v3)
            print('native', v1, time, v3, token)
            data = JSON.parse(JSON.stringify(token))
        })
        return data
    },


    gorgonString: function (input_ints) {
        var result
        Java.perform(function () {
            var o = Java.use('com.ss.a.b.a')
            var js_ints = []
            for (var i = 0; i < input_ints.length; i += 1) {
                js_ints.push(input_ints[i])
            }
            var java_ints = Java.array('byte', js_ints)
            result = o.a(java_ints)
        })
        return result
    }
}
