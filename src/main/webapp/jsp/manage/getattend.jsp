<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.util.ArrayList"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
String date    = request.getParameter("day");
studentDTO dto = new studentDTO();
String checkin = "";
String checkout = "";
ArrayList<attendanceVO> list = dto.GetAttendList(date);
int index = 1;
for(attendanceVO vo : list) {
	String classno	 = vo.getClassno();
	String className = "";
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
	checkin	= vo.getCheckin();
	checkout = vo.getCheckout();

%>
<tr class="ajax_added">
	<td><%= index %></td>
	<td ><a href="studentinfo.jsp?sno=<%= vo.getSno() %>"><%= vo.getSname() %></a></td>
	
	<td><%= className %></td>
	<td><%= date %></td>
	<td>
	    <div class="attendancebox" style="display: flex; justify-content:center;">
	        <div style="width:30%; display: inline-block; text-align:center;">출석</div>
	        <div style="width:30%; display: inline-block; text-align:center;">9:00</div>
	        <div class="exit" style="width:30%; display: inline-block; text-align:center;">18:00</div>  
	    </div>
	</td>
	<td style="border-right: none;" >
		<span>지각</span>
	</td>
</tr>
<%
index += 1;
}
%>