<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@page import="java.util.ArrayList"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
// 한글 인코딩 처리
request.setCharacterEncoding("utf-8");

//studentDTO 객체 생성 및 데이터 읽기
studentDTO dto 	 = new studentDTO();
String status = "1";
ArrayList<studentinfoVO> list = dto.GetList(status);
if( list != null ){
	System.out.println(list.size());
}
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
                top: 100px;
                right: 200px;
                text-align:center;
                border-collapse: collapse;
            }
            tr{ 
                height: 30px; 
                background-color:  #fcfcfc;
            }
            tr:hover{
                background-color: lightgray;
            }
            th{ 
                background-color: #379fc5e7; 
                height: 45px; 
                font-size: 16px;
                border-right: 1px solid darkgray; 
                border-bottom: 1px solid darkgray;
            }
            td{ 
                height: 35px; 
                border-right: 1px solid darkgray; 
                border-bottom: 1px solid darkgray;
            }
            .hovercell:hover{
                background-color: white;
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
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div style="width: 150px; border-right: none; padding-left: 10px;">
                <img src="../../img/logo.png" style="width: 150px;">
            </div>
            <div class="managermenu" style="width:160px;  margin-left:220px; padding-top: 39px;">
                <div style="background-color: #379fc5e7; width:160px; text-align:center; font-size:20px; color:#fcfcfc; border:1px solid darkgray; font-weight:bold; padding:5px 0px;">관리자<br>
                    <a href="managerlogin.jsp" style="color: #fcfcfc;">(로그아웃)</a></div>
                <ul><a href="studentmanage.jsp" class="menu">· 학생관리</a></ul>
                <ul><a href="approve.jsp" class="menu">· 승인대기</a></ul>
                <ul style="border-bottom:1px solid darkgray;"><a href="attendance.jsp" class="menu">· 출결관리</a></ul>
            </div>
				<table>
				    <tr>
				        <td colspan="6" style="text-align: left; padding-bottom: 20px; font-size: 20px; font-weight: bold; padding-bottom: 15px; background-color: white;  border-bottom: 1px solid darkgray; border-right: none;">- 학생관리</td>
				</tr>
				<tr>
				    <th>번호</th>
				    <th>이름</th>
				    <th>수업</th>
				    <th>전화번호</th>
				    <th>생년월일</th>
				    <th style="border-right: none;">등록현황</th>
				</tr>
				<%
				for(studentinfoVO vo : list) {
					String sno = vo.getSno();
				%>
				<form action="deleteOk.jsp" method="post" name="approve">
				<tr>
				    <td><%= sno %></td>
				<td><a href="studentinfo.jsp?sno=<%= vo.getSno() %>" style="text-decoration:none;"><%= vo.getSname() %></a></td>
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
				<td><%= className %></td>
				<td><%= vo.getPhone() %></td>
				<td><%= vo.getBirthday() %></td>
				<td style="border-right: none;">
				    <select style="border-radius: 5px;" name="status">
				                      <option selected value="1">승인</option>
				                      <option value="2">삭제</option>
				                  </select>
				<input type="hidden" name="sno" value="<%= sno %>">
				<button type="submit" onclick="submitOk()" style="width:50px; height:25px; font-weight:bold; background-color: #1895be; border:none; color:white; font-size:12px; border-radius: 5px; cursor:pointer;">확인</button>
				</td>
				</form>
				  </tr>
				<%
				}
				%>
				</table>
        </div>
    </body>
    <script>
        function submitOk() {
            if(confirm("회원을 삭제하시겠습니까?") == true){
                document.approve.submit();
            }
        }
    </script>
</html>