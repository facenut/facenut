<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
    // 한글 인코딩 처리
    request.setCharacterEncoding("utf-8");

    // 폼에서 전달된 sno와 status 파라미터 받기
    String sno = request.getParameter("sno");
    String status = request.getParameter("status");
    String addr = "";
    switch(status) {
    	case "0" :
    		addr = "approve.jsp";
    		break;
    	case "1" :
    		addr = "studentmanage.jsp";
    		break;
    	case "2" :
    		addr = "approve.jsp";
    		break;
    }

    // DTO 객체 생성
    studentDTO dto = new studentDTO();
    studentinfoVO vo = new studentinfoVO();
    if( dto.approve(sno,status) == true) {
		// 변경 성공시
	%>
		<script>
			alert('변경 완료');
    		location.href='<%= addr %>';
    	</script>
	<%
    } else {
    	// 변경 실패시
    	%>
    	<script>
    		alert('변경 실패');
    		location.href='<%= addr %>';
    	</script>
    	<%
    }
%>
