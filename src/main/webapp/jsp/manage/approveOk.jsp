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

    
