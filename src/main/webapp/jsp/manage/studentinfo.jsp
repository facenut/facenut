<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
//한글 인코딩 처리
request.setCharacterEncoding("utf-8");

String sno = request.getParameter("sno");

studentDTO dto = new studentDTO();
studentinfoVO vo = dto.read(sno);
%>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>안면인식 기반 자동출결 시스템</title>
    <style>
        .container {
			background-color: white;
			border-radius: 10px;
			box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 1500px;
            height: 700px;
            margin-left: 190px;
            margin-top: 150px;
            position: relative;
            padding-top: 50px;
		    }
        table{ 
            width:850px;
            position: absolute;
            top: 110px;
            right: 170px;
            text-align:center;
            border-collapse: collapse;
        }
        tr{ 
            height: 30px;
            border: 1px solid darkgray;
            border-left: none;
            border-right: none;
        }
        th{ 
            background-color: #9FC2CE;
            border-right: 1px solid darkgray; 
            border-bottom: 1px solid darkgray;
            font-size: 20px;
        }
        td{ 
            border-bottom: 1px solid darkgray;
            border-right: 1px solid darkgray;
            height: 35px;
        }
        a{
            color: black; 
            text-decoration: none; 
            vertical-align: middle;
        }
        ul{
            width:160px;
            height: 40px;
            font-weight: bold;
            background-color:#fcfcfc;
            margin:0px; 
            padding:0px; text-align:center; 
            font-size:20px;
            border: 1px solid darkgray;
            border-top: none;
           /* border-left:1px solid darkgray;
            border-right:1px solid darkgray; 
            border-bottom: 1px solid darkgray; */
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="width: 150px; border-right: none; padding-left: 10px;">
            <img src="../../img/logo.png" style="width: 150px;">
        </div>
        <div class="managermenu" style="width:160px;  margin-left:220px; padding-top: 37px;">
            <div style="background-color: #379fc5e7; width:160px; text-align:center; font-size:20px; color:#fcfcfc; border:1px solid darkgray; font-weight:bold; padding:5px 0px;">관리자<br>
                <a href="managerlogin.jsp" style="color: #fcfcfc;">(로그아웃)</a></div>
            <ul><a href="studentmanage.jsp" class="menu">· 학생관리</a></ul>
            <ul><a href="approve.jsp" class="menu">· 승인대기</a></ul>
            <ul style="border-bottom:1px solid darkgray;"><a href="attendance.jsp" class="menu">· 출결관리</a></ul>
        </div>
        <form action="modify.jsp" name="student" method="post">
        <input type="hidden" name="sno" value="<%= sno %>">
	        <table>
	            <tr style="border: none;">
	                <td colspan="6" style="text-align: left; font-size: 20px; font-weight: bold; background-color: white; border-right:none;">- 학생정보</td>
	            </tr>
	            <tr>
	                <th style="text-align: center; font-size: 17px;" >이름</th>
	                <td style="text-align: center;"><%= vo.getSname() %></td>
	            </tr>
	            <tr>
	                <th style="text-align: center; font-size: 17px;">강좌</th>
	                <%
					String classno	 = vo.getClassno();
					String className = "";
					if(classno != null || classno != "") {
						switch(classno) {
						    case "1" :
						    	className = "빅데이터";
						    	break;
						    case "2" :
						    	className = "웹디자인";
							    break;
						    case "3" :
						    	className = "AWS";
							    break;
						}
					}
					%>
	                <td style="text-align: center;"><%= className %></td>
	            </tr>
	            <tr>
	                <th style="text-align: center; font-size: 17px;">전화번호</th>
	                <td style="text-align: center;"><%= vo.getPhone() %></td>
	            </tr>
	            <tr>
	                <th style="text-align: center; font-size: 17px;">생년월일</th>
	                <td style="text-align: center;"><%= vo.getBirthday() %></td>
	            </tr>
	            <tr  style="border-bottom: none; ">
	                <td colspan="2" style="border-bottom: none; border-right: none; text-align:right;">
		                <button style="width:60px; height:30px; background-color: #1895be; border:none; font-size:15px; border-radius: 5px; cursor:pointer; color:white; font-weight:bold;" onclick="window.location.href='modify.jsp?sno=<%= vo.getSno() %>'">수정</button>
	                </td>
	            </tr>
	        </table>
	    </form>
        <table style="top: 380px;">
            <tr style="border: none;">
                <td colspan="6" style="text-align: left; font-size: 20px; font-weight: bold; border: none;">- 출결현황</td>
            </tr>
            <tr>
                <th style="height: 45px;">번호</th>
                <th style="height: 45px;">날짜</th>
                <th style="height: 45px;">수강강좌</th>
                <th style="height: 45px;">출결</th>
                <th style="height: 45px;">입실</th>
                <th style="height: 45px; border-right: none;">퇴실</th>
            </tr>
            <tr>
                <td>1</td>
                <td>2025.01.20</td>
                <td>빅데이터</td>
                <td>출석</td>
                <td>9:00</td>
                <td style="border-right: none;">18:00</td>
            </tr>
        </table>
</body>
</html>