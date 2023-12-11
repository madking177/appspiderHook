Java.perform(/*hook string的js方法*/
function hook_string_factory() {
    var StringFactory = Java.use('java.lang.StringFactory');
    StringFactory.newStringFromString.implementation = function (content) {
        console.log("java.lang.StringFactory.newStringFromString->" + content);
        var result = this.newStringFromString(content);
        return result;
    };
})