<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
//한글 인코딩 처리
request.setCharacterEncoding("utf-8");

String sno  = request.getParameter("sno");
String sname  = request.getParameter("username");
String phone = request.getParameter("userphone");
String classno = request.getParameter("classname");

studentinfoVO vo = new studentinfoVO();
vo.setSname(sname);
vo.setPhone(phone);
vo.setClassno(classno);
studentDTO dto = new studentDTO();
if( dto.Changeinfo(sno, sname, phone, classno) == true ){
	// 수정 성공시
			%>
			<script>
				alert('수정이 완료되셨습니다.'); 
				location.href='studentinfo.jsp?sno=<%= sno %>';
			</script>
			<%
		} else {
			// 수정 실패시
			%>
			<script>
				alert('오류가 발생하였습니다. 다시 시도해주세요.'); 
				location.href='modify.jsp';
			</script>
			<%
		}
	%>
