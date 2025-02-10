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
            margin-left:auto;
            margin-right:auto;
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
		<script src="../js/jquery-3.7.1.js"></script>
		<script>
		window.onload = function()
		{
			$("#username").focus();
		}
		
		$(document).ready(function() {
		    $("#joinOk").click(function() {
		        Dosubmit();
		    });
		    
		    $("#joinCancel").click(function() {
				if(confirm("회원 가입을 취소하시겠습니까?") == true)
				{
					document.location = "../html/face/facerecog.html";
				}
			});
		});

		function Dosubmit() {
		    if ($("#username").val() == "") {
		        alert("이름을 입력하세요.");
		        $("#username").focus();
		        return;
		    }
		    if( $("#userphone").val() == "" )
			{
				alert("전화번호를 입력하세요.");
				$("#userphone").focus();
				return;
			}
		 	// 라디오 버튼 선택 여부 확인
	        if ($("input[name='classname']:checked").length == 0) {
	            alert("강좌를 선택하세요.");
	            return;
	        }
		    if( $("#userbirth").val() == "" )
			{
				alert("생년월일을 입력하세요.");
				$("#userbirth").focus();
				return;
			}
		    if(confirm("회원가입을 완료하시겠습니까?")  == true)
			{
				document.forms.student.submit();
			}	
		};
		
		
		</script>
		<section>
        <div class="container">
            <h1></h1>
		<div class="join">회원가입</div>
		<form action="joinOk.jsp" name="student" method="get">
			<table style="width:500px; padding: 50px 50px 0px 50px; margin:0px auto; background-color:white; text-align:center;">
				<tr>
					<th>이름 :</th>
					<td><input type="text" id="username" name="username" style="width:200px;"></td>
				</tr>
				<tr>
					<th>전화번호 :</th>
					<td>
						<input type="text" id="userphone" name="userphone" style="width:200px; padding-top:10px;" maxlength="11"; placeholder="01012345678">
					</td>
				</tr>
				<tr style="height:45px;">
					<th style="padding-top:30px;">강좌명 :</th>
					<td>
						<input type="radio" class="classname" name="classname" value="1" style="padding-top:30px; margin-right:0px;">빅데이터
						<input type="radio" class="classname" name="classname" value="2" style="padding-top:30px; margin-right:0px;">웹디자인
						<input type="radio" class="classname" name="classname" value="3" style="padding-top:30px; margin-right:0px;">AWS
					</td>
				</tr>
				<tr>
					<th>생년월일 :</th>
					<td><input type="text" id= "userbirth" name="userbirth" style="width:200px;" maxlength="8"; placeholder="YYYYMMDD"></td>
				</tr>
				<tr>
                    <td colspan="2" style="padding:65px 0px; padding-right: 1px; border-bottom:none; text-align:center; ">
                        <button type="button" id="joinOk" style="color:white; text-decoration:none;">가입완료</button>
                        <button type="button" id="joinCancel" style="color:white; text-decoration:none;">가입취소</button>
                    </td>
                </tr>
			</table>
		</form>
		<div style="width: 150px; border-right: none; padding-left: 181px;">
            <img src="../img/logo.png" style="width: 120px;">
        </div>
		</section>
	</body>
</html>