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

