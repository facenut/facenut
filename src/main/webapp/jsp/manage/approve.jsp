<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
// 한글 인코딩 처리
request.setCharacterEncoding("utf-8");

// sno와 status 값을 URL 파라미터로 받음
String sno = request.getParameter("sno");
String status = request.getParameter("status");

if (sno == null || status == null) {
    out.print("<script>alert('잘못된 접근입니다.'); history.back();</script>");
    return;
}

// studentDTO 객체 생성
studentDTO dto = new studentDTO();
studentinfoVO vo = null;

// 상태 업데이트: 상태를 변경하는 메서드 호출
boolean isUpdated = dto.updateStatus(sno, status);

// 상태 업데이트 후 학생 정보 가져오기
if (isUpdated) {
    vo = dto.read(sno);  // 상태 변경 후 학생 정보 조회
} else {
    // 상태 변경 실패시 처리
    out.print("<script>alert('상태 변경에 실패했습니다.'); history.back();</script>");
    return;
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
        table {
            width: 850px;
            position: absolute;
            top: 100px;
            right: 200px;
            text-align: center;
            border-collapse: collapse;
        }
        tr {
            height: 30px;
            background-color: #fcfcfc;
        }
        tr:hover {
            background-color: lightgray;
        }
        th {
            background-color: #379fc5e7;
            height: 45px;
            font-size: 16px;
            border-right: 1px solid darkgray;
            border-bottom: 1px solid darkgray;
        }
        td {
            height: 35px;
            border-right: 1px solid darkgray;
            border-bottom: 1px solid darkgray;
        }
        .hovercell:hover {
            background-color: white;
        }
        a {
            color: black;
            text-decoration: none;
            vertical-align: middle;
        }
        ul {
            width: 160px;
            height: 40px;
            font-weight: bold;
            background-color: #fcfcfc;
            margin: 0px;
            padding: 0px;
            text-align: center;
            font-size: 20px;
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
        <div class="managermenu" style="width:160px; margin-left:220px; padding-top: 39px;">
            <div style="background-color: #379fc5e7; width:160px; text-align:center; font-size:20px; color:#fcfcfc; border:1px solid darkgray; font-weight:bold; padding:5px 0px;">관리자<br>
                <a href="managerlogin.jsp" style="color: #fcfcfc;">(로그아웃)</a></div>
            <ul><a href="studentmanage.jsp" class="stumenu">· 학생관리</a></ul>
            <ul><a href="approve.jsp" class="appmenu">· 승인대기</a></ul>
            <ul style="border-bottom:1px solid darkgray;"><a href="attendance.jsp" class="attmenu">· 출결관리</a></ul>
        </div>
        <form action="approveOk.jsp" method="post" name="student">
            <table>
                <tr>
                    <td colspan="6" style="text-align: left; padding-bottom: 20px; font-size: 20px; font-weight: bold; padding-bottom: 15px; background-color: white; border-right: none;">- 승인대기</td>
                </tr>
                <tr>
                    <th>번호</th>
                    <th>이름</th>
                    <th>수업</th>
                    <th>전화번호</th>
                    <th>생년월일</th>
                    <th style="border-right: none;">등록현황</th>
                </tr>
                <tr>
                    <td><%= vo.getSno() %></td>
                    <td><a style="text-decoration:none;"><%= vo.getSname() %></a></td>
                    <td><%= vo.getClassno() %></td>
                    <td><%= vo.getPhone() %></td>
                    <td><%= vo.getBirthday() %></td>
                    <td style="border-right: none;">
                        <select style="border-radius: 5px;" name="status">
                            <option <% if(vo.getStatus().equals("0")) out.print("selected"); %> value="0">대기</option>
                            <option <% if(vo.getStatus().equals("1")) out.print("selected"); %> value="1">승인</option>
                            <option <% if(vo.getStatus().equals("2")) out.print("selected"); %> value="2">삭제</option>
                        </select>
                    </td>
                </tr>
            </table>
            <input type="hidden" name="sno" value="<%= vo.getSno() %>">
            <button type="button" onclick="submitOk()" style="width:95px; height:35px; font-weight:bold; background-color: #1895be; border:none; color:white; font-size:15px; border-radius: 5px; position:absolute; bottom: 190px; right:563px; cursor:pointer;">확인</button>
        </form>
    </div>
</body>
<script>
    function submitOk() {
        if(confirm("회원을 승인하시겠습니까?") == true){
            document.student.submit();
        }
    }
</script>
</html>
