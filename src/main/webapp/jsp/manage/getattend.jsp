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

ArrayList<attendanceVO> refine_list = new ArrayList<>();

attendanceVO before = new attendanceVO();

ArrayList<String> events =new ArrayList<>();

// 새 리스트 만들기
for(attendanceVO vo : list){
	System.out.println(before.getSno()+ " " +vo.getSno() + " " + vo.getEvent() );
	if(vo.getSno().equals(before.getSno())){
		// 앞 vo와 지금 vo가 같으면 -> 기존 checkin 시간을 땡겨옴
		System.out.println("체크인 갱신");
		vo.setCheckin(before.getCheckin());
		
		// 기존 vo에서 events를 가져오고
		ArrayList<String> tmp = null;
		if(before.getEvents() != null){
			tmp = before.getEvents();
			// 지금 vo의 event를 events에 넣고
			tmp.add(vo.getEvent());
			// 지금 vo의 events에 넣음
			vo.setEvents(tmp);
		}
		before = vo;
	}else if(before.getSno() != null){
		// 다르면, refine_list에 기존vo를 넣고, 다음 반복으로 넘어갑니다
		System.out.println("리스트에 vo add");
		refine_list.add(before);
		
		ArrayList<String> tmp = new ArrayList<>();
		tmp.add(vo.getEvent());
		vo.setEvents(tmp);
		before = vo;
		
	}else{
		// 지금 vo가 첫번째 vo임
		ArrayList<String> tmp = new ArrayList<>();
		tmp.add(vo.getEvent());
		vo.setEvents(tmp);
		before = vo;
	}
}
// 마지막 vo를 리스트에 넣음
refine_list.add(before);



System.out.println("새로 만든 리스트 원소 개수 : " + refine_list.size());
for(attendanceVO vo : refine_list){
	System.out.println("******************");
	System.out.println(vo.toString());
	System.out.println("******************");
}

int index = 1;
for(attendanceVO vo : refine_list) {
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
	String event_str = "";
	// events에서 event를 검색 -> '불인정' -> event : 결석
	for(String event : vo.getEvents()){
		System.out.println(event);
		if(event.equals("불인정")){
			event_str = "결석";
			break;
		}else if(event.equals("복귀")){
			event_str = "외출";
			break;
		}else if(event.equals("조퇴")){
			event_str = "조퇴";
			break;
		}else if(event.equals("지각")){
			event_str = "지각";
			break;
		}else{
			event_str = "출석";
		}
		
	}
	
%>
<tr class="ajax_added">
	<td><%= index %></td>
	<td ><a href="studentinfo.jsp?sno=<%= vo.getSno() %>"><%= vo.getSname() %></a></td>
	
	<td><%= className %></td>
	<td><%= date %></td>
	<td>
	    <div class="attendancebox" style="display: flex; justify-content:center;">
	        <div style="width:30%; display: inline-block; text-align:center;"><%= vo.getEvent() %></div>
	        <div style="width:30%; display: inline-block; text-align:center;"><%= vo.getCheckin().split(" ")[1] %></div>
	        <div class="exit" style="width:30%; display: inline-block; text-align:center;"><%= vo.getCheckout().split(" ")[1] %></div>  
	    </div>
	</td>
	<td style="border-right: none;" >
		<span><%= event_str %></span>
	</td>
</tr>
<%
index += 1;
}
%>