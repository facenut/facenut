<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@page import="ezen.dto.*"%>
<%@page import="ezen.vo.*"%>
<%
studentDTO dto = new studentDTO();
studentinfoVO vo = dto.read("sno");
%>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>안면인식 기반 자동출결 시스템</title>
	</head>
	<body>
		<style>
			.modify{
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
			<div class="modify">회원수정</div>
			<form action="modifyok.jsp" name="user" id="user" method="get">
				<table style="width:500px; padding: 50px 50px 0px 50px; margin:0px auto; background-color:white; text-align:center;">
					<tr>
						<th>이름 :</th>
						<td><input type="text" id="userName" name="username" style="width:200px;"><% vo.getSname(); %></td>
					</tr>
					<tr>
						<th>전화번호 :</th>
						<td>
							<input type="text" id="userphone" name="userphone" style="width:200px; padding-top:10px;"><% vo.getPhone(); %>
						</td>
					</tr>
					<tr style="height:45px;">
						<th style="padding-top:30px;">강좌명 :</th>
						<td><input type="text" id="classname" name="classname" style="width:200px; padding-top:30px;"><% vo.getClassno(); %></td>
					</tr>
					<tr>
						<th>생년월일 :</th>
						<td><input type="text" id= "userbirth" name="userbirth" style="width:200px;"><% vo.getBirthday(); %></td>
					</tr>
					<tr>
	                    <td colspan="2" style="padding:65px 0px; padding-right: 1px; border-bottom:none; text-align:center; ">
	                        <button class="button" onclick="modifyok()" style="color:white; text-decoration:none;">수정완료</button>
	                        <button type="button" id="joinCancel" onclick="DoCancel()" style="color:white; text-decoration:none;">수정취소</button>
	                    </td>
	                </tr>
				</table>
			</form>
			<div style="width: 150px; border-right: none; padding-left: 181px;">
	            <img src="../../img/logo.png" style="width: 120px;">
	        </div>
	    </div>
		</section>
	</body>
	<script>
		function modifyok() {
			if(confirm("회원을 수정하시겠습니까?") == true){
				document.modify.submit();
			}
		}
		function DoCancel() {
			location.href="studentinfo.jsp";
		}

	</script>
</html>