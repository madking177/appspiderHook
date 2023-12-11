Java.perform(
    function () {
        console.log("############################ Frida 开启 ############################");
        /* 此处是 hook 关闭 spdy 协议 */
        const switchConfigSession = Java.use("mtopsdk.mtop.global.SwitchConfig");
        if (switchConfigSession) {
            console.log("------>定位到类名: ${switchConfigSession}", switchConfigSession);
            switchConfigSession.q.implementation = function () {
                console.log("------>定位到函数: is_enableSpdy");
                return false;
            }
        }
    }
)
//

