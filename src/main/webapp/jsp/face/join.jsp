<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>안면인식 회원가입</title>
	</head>
	<body>
		<style>
			.join{
				font-weight:bold;
			    font-size:30px;
			    text-align:center;
			    margin:50px auto;
			    padding: 50px 0px 0px 10px;
			}
            .container {
			background-color: white;
			border-radius: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 500px;
            height: 600px;
            text-align: center;
            margin-top:150px;
            margin-left:700px;
            position: relative;
		    }
			tr{ height:39px; text-align:center; }
			th{
				width: 30%;
				text-align:left
                
			}
			td{
				width:70%;
				border-bottom:1px solid black; 
			}
            button{
                background-color:#0fa8d9;
                color:white;
	            width:110px; 
	            height:35px; 
	            font-size:15px;
	            font-weight:bold;
	            cursor:pointer;
				border-radius:5px;
	            border:none;
				text-decoration: none;

            }
            input{
	            border:none;
	            font-size:16px;
	            font-family: 'Raleway', sans-serif;
				margin-right: 55px;
            }
            input:focus{ outline:none; }   
		</style>
		<section>
        <div class="container">
            <h1></h1>
		<div class="join">회원가입</div>
		<form action="#" name="user" method="post">
			<table style="width:500px; padding: 50px 50px 0px 50px; margin:0px auto; background-color:white; text-align:center;">
				<tr>
					<th>이름 :</th>
					<td><input type="text" id="userName" name="username" style="width:200px;"></td>
				</tr>
				<tr>
					<th>전화번호 :</th>
					<td>
						<input type="text" id="userphone" name="userphone" style="width:200px; padding-top:10px;">
					</td>
				</tr>
				<tr style="height:45px;">
					<th style="padding-top:30px;">강좌명 :</th>
					<td><input type="text" id="classname" name="classname" style="width:200px; padding-top:30px;"></td>
				</tr>
				<tr>
					<th>생년월일 :</th>
					<td><input type="text" id= "userbirth" name="userbirth" style="width:200px;"></td>
				</tr>
				<tr>
                    <td colspan="2" style="padding:80px 0px; padding-right: 1px; border-bottom:none; text-align:center; ">
                        <button type="button" class="button" onclick="joinok();" style="color:white; text-decoration:none;">가입완료</button>
                        <button type="button" id="joinCancel" onclick="DoCancel()" style="color:white; text-decoration:none;">가입취소</button>
                    </td>
                </tr>
			</table>
		</form>
		</section>
		<script>
			function joinok() {
				if(confirm("회원가입을 완료하시겠습니까?") == true){
					document.user.submit();
				}
			}
			function DoCancel() {
				location.href="faceregist.html";
			}
		</script>
	</body>
</html>