function bindEmailCodeClick() {
    $('#send-code').click(function(event) {
        event.preventDefault();

        let that = $(this);
        let email = $("#reg-email").val();
        let emailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$/;

        if (!emailReg.test(email)) {
            alert("请输入合法的邮箱");
            return;
        }

        // 倒计时的过程取消点击事件
        that.off('click');

        // 倒计时
        let countdown = 60;
        that.text(countdown + "s");
        that.prop('disabled', true);

        let timer = setInterval(function() {
            countdown -= 1;
            that.text(countdown + "s");

            if (countdown <= 0) {
                that.text("获取验证码");
                that.prop('disabled', false);
                clearInterval(timer);
                bindEmailCodeClick();
            }
        }, 1000);

        $.ajax({
            url: "/email/code",
            type: "GET",
            data: { "email": email },
            dataType: "json",
            success: function(response) {
                console.log("服务器返回:", response);

                // 修改这里：根据后端实际返回判断
                if (response.result === true) {
                    alert("✅ 验证码已发送到您的邮箱，请查收");
                } else {
                    // 发送失败，重置按钮
                    alert("❌ " + (response.message || "发送失败，请稍后重试"));
                    clearInterval(timer);
                    that.text("获取验证码");
                    that.prop('disabled', false);
                    bindEmailCodeClick();
                }
            },
            error: function(xhr, status, error) {
                console.error("请求失败:", xhr.responseText);
                alert("❌ 网络错误，请检查网络连接");
                clearInterval(timer);
                that.text("获取验证码");
                that.prop('disabled', false);
                bindEmailCodeClick();
            }
        });
    });
}
function bindRegisterEvent() {
    $("#submit-btn").click(function(event) {
        event.preventDefault();
        let email = $("#reg-email").val();
        let code = $("#reg-code").val();
        let username = $("#reg-username").val();
        let password = $("#reg-password").val();
        let confirm_passwd = $("#reg-confirm-password").val();
        if(password != confirm_passwd) {
            alert("两次密码不一致")
            return;

        }
        $.post({
            url: "/register",
            data: {email: email, code: code, username: username, password: password},
            success: function(response) {
                if (response.result === true) {
                    window.location="/login";
                }else{
                    let message = response["message"];
                    alert(message);
                }
            }
        })
    })
}



$(function() {
    bindEmailCodeClick();
    bindRegisterEvent();
});