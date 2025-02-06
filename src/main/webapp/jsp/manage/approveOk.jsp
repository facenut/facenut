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

    // DAO 객체 생성
    studentDTO dto = new studentDTO();

    // 학생 상태 업데이트
    boolean result = dto.updateStatus(sno, status);

    if (result) {
        out.println("<script>alert('상태가 성공적으로 변경되었습니다.'); location.href='approve.jsp';</script>");
    } else {
        out.println("<script>alert('상태 변경에 실패했습니다.'); history.back();</script>");
    }
%>
