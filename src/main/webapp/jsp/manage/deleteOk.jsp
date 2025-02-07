<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %> 
<% 
String sno = request.getParameter("sno");
String status = request.getParameter("status");

studentDTO dto 	 = new studentDTO();

if( dto.delete(sno, status) == true ) {
	// 회원정보 삭제
	out.print("PASS");
	return;
}

out.print("ERROR");
%>