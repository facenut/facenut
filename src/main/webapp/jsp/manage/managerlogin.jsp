<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>안면인식 기반 자동출결 시스템</title>
	</head>
	<body>
		<style>
			.managerpw{
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
				width:70%;
                height:70px;
                font-size:30px ;
                border-radius: 5px;
				background-color:#0fa8d9; 
                text-align: center;
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
            }
            input:focus{ outline:none; }   
		</style>
		<section>
        <div class="container">
            <h1></h1>
		<div class="managerpw">관리자 비밀번호</div>
		<form action="#" name="user" method="post">
			<table style="width:400px; padding: 85px 50px 0px 50px; margin:0px auto; background-color:white; text-align:center;">
				<tr>
					<th><input type="password" id= "managerpw" name="managerpw" style="width:200px; background-color: #0fa8d9;"></th>
				</tr>
				<tr>
                    <td colspan="2" style="padding:150px 0px 30px 0px; padding-right: 1px; border-bottom:none; text-align:center; ">
                        <button id="managerpwok"><a href="studentmanage.jsp" style="color:white; text-decoration:none; ">확인</a></button>
                    </td>
                </tr>
			</table>
		</form>
		<div style="width: 150px; border-right: none; padding-left: 181px;">
            <img src="../../img/logo.png" style="width: 120px;">
        </div>
		</section>
	</body>
</html>