//注册------------------------------------------start
//点击注册 事件
$("#btn_login").on("click",function () {
        var infoCheck = true;
        if($("#i_user").val() == "")infoCheck = false;
        if($("#i_password").val() == "")infoCheck = false;
        if($("#i_repassword").val() == "")infoCheck = false;
        if($("#i_email").val() == "")infoCheck = false;
        if(infoCheck) {
            $.ajax({
                url: "/login/",
                type: "GET",
                data: {
                    what: "login",
                    user: $("#i_user").val(),
                    password: $("#i_password").val(),
                    email: $("#i_email").val(),
                    gender: $("input:radio[name='gender']:checked").val()
                },
                success: function (data) {
                    if (data == "True") {
                        alert("注册成功");
                        $("#login_modal").modal('hide');
                    } else {
                        alert(data);
                    }

                }
            })
        }
    })
    $("#i_user").on("blur",function () {
        if($(this).val() != "") {
            $.ajax({
                url: "/login/",
                type: "GET",
                data: {what: "userCheck", userName: $("#i_user").val()},
                success: function (data) {
                    if (data != "OK") {
                        $("#i_user_check").removeClass("hidden");
                        $("#i_user_ok").addClass("hidden");
                        $("#i_user_check").text(data);
                    } else {
                        $("#i_user_check").addClass("hidden");
                        $("#i_user_ok").removeClass("hidden");
                        $("#i_user_check").text("");
                    }
                }
            })
        }
    })
    $("#i_repassword,#i_password").on("blur",function () {
        if ( $("#i_repassword").val() != "" & $("#i_password").val() != ""){
            if($("#i_repassword").val() != $("#i_password").val()) {
                $("#i_password_check").removeClass("hidden");
                $("#i_password_ok").addClass("hidden");
                $("#i_password_check").text("两次密码不相同");
            } else {
                $("#i_password_check").addClass("hidden");
                $("#i_password_ok").removeClass("hidden");
                $("#i_password_check").text("");
            }
        }
    })
    $("#i_email").on("blur",function () {
        if($("#i_email").val() != ""){
            var email = $("#i_email").val();
            if(!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
                $("#i_email_check").removeClass("hidden");
                $("#i_email_ok").addClass("hidden");
                $("#i_email_check").text("格式不正确!请重新输入");
            }
            else {
                $("#i_email_check").addClass("hidden");
                $("#i_email_ok").removeClass("hidden");
                $("#i_email_check").text("");
            }
        }

    })
//注册------------------------------------------end
//登录------------------------------------------start
//点击登录事件
$("#btn_logup").on("click",function () {
    if ($("#i_user_up").val() == ""){
        $("#logup_check").removeClass("hidden");
        $("#logup_check").text("用户名不能为空");
        return;
    }
    else if($("#i_password_up").val() == ""){
        $("#logup_check").removeClass("hidden");
        $("#logup_check").text("密码不能为空");
        return;
    }
    else {
        $("#logup_check").addClass("hidden");
        $("#logup_check").text("");
    }
    $.ajax({
        url: "/login/",
        type: "GET",
        data: {
            what: "logup",
            userName: $("#i_user_up").val(),
            password: $("#i_password_up").val()
        },
        success: function (data){
            console.log("function -> 点击登录事件() -----");
            if (data="登录成功"){
                $("#logup_check_ok").removeClass("hidden");
                $("#logup_check_ok").text("登录成功");
                getHeadIcon($("#i_user_up").val());
                window.location.reload();//刷新页面
            }
            else{
                $("#logup_check").removeClass("hidden");
                $("#logup_check").text(data);
            }
        }
    })
})

function myAutoLogin() {
    $.ajax({
        url: "/login/",
        type: "GET",
        data: {
            what: "autoLogin"
        },
        success: function (data){
            console.log("function -> myAutoLogin() -----");
            console.log(data);
            var obj =  $.parseJSON(data);
            console.log(obj);
            console.log(obj['status']);
            console.log(obj['userName']);
            if(obj['status'] == "activate"){
                $("#log_button").addClass("hidden");
                $("#login_userInfo").removeClass("hidden");
                $("#login_userInfo_userName").text(obj['userName']);
                getHeadIcon(obj['userName']);
            }
        }
    })
}
myAutoLogin();
//登录------------------------------------------end
//获取头像------------------------------------------start
function getHeadIcon(userName) {
    $.ajax({
         url: "/login/",
         type: "GET",
         data: {
             what: "getHeadIcon",
             userName:userName
         },
         success: function (data) {
             if(data == "notheadIcon"){
                $("#userHeadIcon").attr('src','/static/img/headIcon/man.png');
                // window.location.reload();//刷新页面
             }
             else {
                console.log(data)
                $("#userHeadIcon").attr('src',data);

                // window.location.reload();//刷新页面
             }

         }
     })
}
//获取头像------------------------------------------end
//注销------------------------------------------start
$("#logout_button").on("click",function () {
     // $.session.clear();
     $.ajax({
         url: "/login/",
         type: "GET",
         data: {
             what: "logout"
         },
         success: function (data) {
             window.location.reload();//刷新页面
         }
     })
})
//注销------------------------------------------end