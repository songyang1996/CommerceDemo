$(document).ready(function() {
  $('#btnLogin').click(function () {
                // 1.获取输入的数据
                username = $('#username').val()
                password = $('#pwd').val()
                csrf = $('input[name="csrfmiddlewaretoken"]').val()
                remember = $('input[name="remember"]').prop('checked')
                // alert(remember)
                // 2.发起ajax请求
                params = {'username':username, 'password':password,
                        'csrfmiddlewaretoken':csrf, 'remember':remember}
                $.post('/user/login_handle/', params, function (data) {
                    // 登录成功 {'res':1}
                    // 登录失败 {'res':0}
                    if (data.res == 0){
                        $('#username').next().html('用户名或密码错误').show()
                    }
                    else
                    {
                        // 跳转页面
                        location.href = data.next_url  // /user/address/
                    }
                })
            })
});
