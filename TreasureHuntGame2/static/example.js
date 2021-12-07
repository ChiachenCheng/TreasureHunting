var words = document.getElementById("top");

function signup(event) {
	var user_elem = document.getElementById("signup_user");
	var user = user_elem.value;
	var pass_elem = document.getElementById("signup_passwd");
	var pass = pass_elem.value;
	var pass_elem_again = document.getElementById("signup_passwd_again");
	var pass_again = pass_elem_again.value;
	if(user == ""){
		alert('请输入用户名！');
		return;
	}
	if(pass == ""){
		alert('请输入密码！');
		return;
	}
	if(pass != pass_again){
		alert('兩次輸入的密碼不一致！');
		return;
	}
	$.ajax({
		type: "POST",
		url: "signup",
		data: {
			username: user,
			password: pass
		},
		dataType: "json",
		success: function (data) {
			
			if(data['success'] == 0) {
				alert('用户已存在');
			}
			else {
				alert('注册成功');
				user_elem.value = "";
				pass_elem.value = "";
				pass_elem_again.value = "";
			}
		},
		error: function (htp, s, e) {
			alert('注册失败');
		}
	});
}

function login(event) {
	var user_elem = document.getElementById("login_user");
	var user = user_elem.value;
	var pass_elem = document.getElementById("login_passwd")
	var pass = pass_elem.value;
	if(user==""){
		alert('用户名为空！');
		return;
	}
	if(pass==""){
		alert('密码为空！');
		return;
	}
	$.ajax({
		type: "POST",
		url: "login",
		data: {
			username: user,
			password: pass
		},
		dataType: "json",
		success: function (data) {
			if(data['success'] == 0) {
				alert('用户不存在，请注册/密碼錯誤，請重試');
			}
			else {
				alert('登录成功！')
				// words.innerHTML = "你好，" + user + "!";
				// user_elem.value = "";
				window.location.href = "operation/" + user
			}
			
		},
		error: function (htp, s, e) {
			alert('登录失败');
		}
	});
}