<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@page import="ezen.dto.studentDTO"%>
<%@page import="ezen.vo.studentinfoVO"%>
<% 
//한글 인코딩 처리
request.setCharacterEncoding("utf-8");

String username = request.getParameter("username");
String userphone = request.getParameter("userphone");
String classname = request.getParameter("classname");
String userbirth = request.getParameter("userbirth");

studentinfoVO vo = new studentinfoVO();
vo.setSname(username);
vo.setPhone(userphone);
vo.setClassno(classname);
vo.setBirthday(userbirth);

studentDTO dto = new studentDTO();
if( dto.join(vo) == true )
{
	// 가입 성공시
	%>
	<script>
		alert('회원으로 가입되셨습니다.'); location.href='facerecog.html';
	</script>
	<%
} else {
	// 가입 실패시
	%>
	<script>
		alert('오류가 발생하였습니다. 다시 시도해주세요.'); location.href='facerecog.html';
	</script>
	<%
}
%>
