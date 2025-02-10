<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@page import="java.util.ArrayList"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
//한글 인코딩 처리
request.setCharacterEncoding("utf-8");

studentDTO dto = new studentDTO();
studentinfoVO vo = new studentinfoVO();
attendanceVO VO = new attendanceVO(); 
String status = "1";
ArrayList<studentinfoVO> list = dto.GetList(status);
if( list != null ){
	System.out.println(list.size());
}
%>


<!DOCTYPE html>
<html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>안면인식 기반 자동출결 시스템</title>
        <script src="../../js/jquery-3.7.1.js"></script>
        <script type="text/javascript">
	        window.onload = function() {
		        var start_year="2024";// 시작할 년도
		        var today = new Date();
		        var today_year= today.getFullYear();
		        var index=0;
		        for(var y=start_year; y<=today_year; y++){ //start_year ~ 현재 년도
		        	document.getElementById('select_year').options[index] = new Option(y, y);
		        	index++;
		        }
		        index=0;
		        for(var m=1; m<=12; m++){
		        	document.getElementById('select_month').options[index] = new Option(m, m);
		        	index++;
		        }
		
		        lastday();
		        let request_date = ""
		        const select_day = document.getElementById("select_day");
		        select_day.addEventListener("change", function(e) {
		            selected_day = "< "+$("#select_year").val()+"년 "+$("#select_month").val()+"월 "+$("#select_day").val()+"일 출석현황 >"
		            request_date = $("#select_year").val()+"-"+$("#select_month").val()+"-"+$("#select_day").val()
		            $("#selected_day").html(selected_day);
		            
		            $.ajax({
		        		url : 'getattend.jsp?day=' + request_date,
		        		type : 'get',
		        		success : function(result) {
		        			if($(".ajax_added")) $(".ajax_added").remove(); 
		        			$("#add_list_after_here").after(result)
		        		}
		        	});
		        });
		        $("#CheckBtn").click(function() {
		        	request_date = $("#select_year").val()+"-"+$("#select_month").val()+"-"+$("#select_day").val()
		            $("#selected_day").html(selected_day);
		            
		            $.ajax({
		        		url : 'getattend.jsp?day=' + request_date,
		        		type : 'get',
		        		success : function(result) {
		        			if($(".ajax_added")) $(".ajax_added").remove(); 
		        			$("#add_list_after_here").after(result)
		        		}
		        	});
				});
	        }

	        function lastday(){ //년과 월에 따라 마지막 일 구하기 
	        	var Year=document.getElementById('select_year').value;
	        	var Month=document.getElementById('select_month').value;
	        	var day=new Date(new Date(Year,Month,1)-86400000).getDate();
	            /* = new Date(new Date(Year,Month,0)).getDate(); */
	            
	        	var dayindex_len=document.getElementById('select_day').length;
	        	if(day>dayindex_len){
	        		for(var i=(dayindex_len+1); i<=day; i++){
	        			document.getElementById('select_day').options[i-1] = new Option(i, i);
	        		}
	        	}
	        	else if(day<dayindex_len){
	        		for(var i=dayindex_len; i>=day; i--){
	        			document.getElementById('select_day').options[i]=null;
	        		}
	        	}
	        }
	        
        </script>
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
            table{ 
                width:850px;
                position: absolute;
                top: 100px;
                right: 200px;
                text-align:center;
                border-collapse: collapse;
            }
            tr{ height: 32px; background-color:  #fcfcfc;}
            th{ background-color: #9FC2CE;
                height: 33px; 
                font-size: 16px;
                border-bottom: 1px solid darkgray;
                border-right: 1px solid darkgray;
            }
            td{ border-bottom: 1px solid darkgray; 
                height: 35px;
                border-bottom: 1px solid darkgray;
                border-right: 1px solid darkgray; 
            }
            tr:hover{
                background-color: lightgray;
            }
            .hovercell:hover{
                background-color: white;
            }
            a{
                color: black; 
                text-decoration: none; 
                vertical-align: middle;
            }
        
            ul{
                width:160px;
                height: 40px;
                font-weight: bold;
                background-color:#fcfcfc;
                margin:0px; 
                padding:0px; text-align:center; 
                font-size:20px; 
                border: 1px solid darkgray;
                border-top: none;
            }
            div{
                border-right: 1px solid darkgray;
            }
            .attendancebox, .exit, .container{
                border-right:none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div style="width: 150px; border-right: none; padding-left: 10px;">
                <img src="../../img/logo.png" style="width: 150px;">
            </div>
            <div class="managermenu" style="width:160px; border-right:none;  margin-left:220px; padding-top: 39px;">
                <div style="background-color:   #379fc5e7; width:160px; text-align:center; font-size:20px; color:#fcfcfc; border:1px solid darkgray; font-weight:bold; padding:5px 0px;">관리자<br>
                    <a href="managerlogin.jsp" style="color: #fcfcfc;">(로그아웃)</a></div>
                <ul><a href="studentmanage.jsp" class="menu">· 학생관리</a></ul>
                <ul><a href="approve.jsp" class="menu">· 승인대기</a></ul>
                <ul style="border-bottom:1px solid darkgray;"><a href="attendance.jsp" class="menu">· 출결관리</a></ul>
            </div>
            <table>
                <tr>
                    <td colspan="6" style="text-align: left; padding-bottom: 20px; font-size: 20px; font-weight: bold; border: none; background-color: white;">- 출결관리</td>
                </tr>
                <tr style="height:40px; background-color: #9FC2CE; border-bottom:1px solid black;">
                    <td colspan="3" style="border-bottom: 1px solid darkgray; border-top: 1px solid darkgray; border-right: none; border-left: none; text-align:left; font-weight:bold; padding-left:30px; ">
						날짜 :  <select id="select_year" onchange="javascript:lastday();" style="border-radius: 5px;"></select>년
								<select id="select_month" onchange="javascript:lastday();" style="border-radius: 5px;"></select>월
								<select id="select_day" style="border-radius: 5px;"></select>일
								<button class="button" type="button" id="CheckBtn">조회</button>
                    </td>
                    <td colspan="3" style="border-bottom: 1px solid darkgray; border-top: 1px solid darkgray; border-left: none; border-right: none;text-align:left; font-weight:bold; padding-left: 15px;">
                        <div id="selected_day" style="text-size:20px;"></div>
                    </td>
                </tr>
                <tr>
                    <th rowspan="2" style="width: 80px; border-left: 2px solid darkgray; border-left: none;">번호</th>
                    <th rowspan="2">이름</th>
                    <th rowspan="2">수업</th>
                    <th rowspan="2">날짜</th>
                    <th>출결</th>
                    <th rowspan="2" style= "border-right: 2px solid darkgray; border-right: none;">출결 상태</th>
                </tr>
                <tr style="border-bottom: 2px solid darkgray;" id="add_list_after_here">
                    <td style="border-bottom: none; background-color:#9FC2CE;">
                        <div class="attendancebox" style="display: flex; justify-content:center; border-right: none;">
                            <div style="width:30%; display: inline-block; text-align:center; font-weight:bold; padding: 7px 0px; color: white; ">입실</div>
                            <div class="exit" style="width:30%; display: inline-block; text-align:center; font-weight:bold; padding: 7px 0px; color: white;">퇴실</div>  
                        </div>
                    </td>
                </tr>
                <tr>
                    <td><%= VO.getIdx() %></td>
                    <td ><a href="studentinfo.jsp?sno=<%= vo.getSno() %>" ><%= vo.getSname() %></a></td>
                    <%
					String classno	 = vo.getClassno();
					String className = "";
					if(classno != null || classno != "") {
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
					}
					%>
					<td><%= className %></td>
                    <td>25.01.20</td>
                    <td>
                        <div class="attendancebox" style="display: flex; justify-content:center;">
                            <div style="width:30%; display: inline-block; text-align:center;"><%= VO.getChecktime() %></div>
                            <div class="exit" style="width:30%; display: inline-block; text-align:center;"><%= VO.getChecktime() %></div>  
                        </div>
                    </td>
                    <td style="border-right: none;" >
                        <span>지각</span>
                       <!--  <span>지0</span>
                        <span>외0</span>
                        <span>결0</span> -->
                    </td>
                </tr>
            </table>
        </div>
    </body>
</html>