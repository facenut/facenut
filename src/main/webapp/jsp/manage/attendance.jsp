<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="ezen.dao.*" %>
<%@ page import="ezen.dto.*" %>
<%@ page import="ezen.vo.*" %>
<%
//한글 인코딩 처리
request.setCharacterEncoding("utf-8");

// 폼에서 전달된 sno와 status 파라미터 받기
String sno = request.getParameter("sno");
%>


<!DOCTYPE html>
<html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>안면인식 기반 자동출결 시스템</title>
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
            th{ background-color: #379fc5e7; 
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
                <div style="background-color: #379fc5e7; width:160px; text-align:center; font-size:20px; color:#fcfcfc; border:1px solid darkgray; font-weight:bold; padding:5px 0px;">관리자<br>
                    <a href="managerlogin.jsp" style="color: #fcfcfc;">(로그아웃)</a></div>
                <ul><a href="studentmanage.jsp" class="menu">· 학생관리</a></ul>
                <ul><a href="approve.jsp" class="menu">· 승인대기</a></ul>
                <ul style="border-bottom:1px solid darkgray;"><a href="attendance.jsp" class="menu">· 출결관리</a></ul>
            </div>
            <table>
                <tr>
                    <td colspan="6" style="text-align: left; padding-bottom: 20px; font-size: 20px; font-weight: bold; border: none; background-color: white;">- 출결관리</td>
                </tr>
                <tr style="height:40px; background-color: #379fc5e7; border-bottom:1px solid black;">
                    <td colspan="2" style="border-bottom: 1px solid darkgray; border-top: 1px solid darkgray; border-right: none; border-left: none; text-align:left; font-weight:bold; padding-left:30px; ">
                        날짜
                        <select style="border-radius: 5px;">
                            <option>25.01.20</option>
                            <option>25.01.19</option>
                            <option>25.01.18</option>
                            <option>25.01.17</option>
                            <option>25.01.16</option>
                        </select>
                    </td>
                    <td colspan="4" style="border-bottom: 1px solid darkgray; border-top: 1px solid darkgray; border-left: none; border-right: none;text-align:left; font-weight:bold; padding-left: 15px;">
                        학생
                        <select style="border-radius: 5px;">
                            <option>전체</option>
                            <option>홍길동</option>
                            <option>홍길동</option>
                            <option>홍길동</option>
                            <option>홍길동</option>
                            <option>홍길동</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <th rowspan="2" style="width: 80px; border-left: 2px solid darkgray; border-left: none;">번호</th>
                    <th rowspan="2">이름</th>
                    <th rowspan="2">수업</th>
                    <th rowspan="2">날짜</th>
                    <th>출결</th>
                    <th rowspan="2" style= "border-right: 2px solid darkgray; border-right: none;">이용자 통계</th>
                </tr>
                <tr style="border-bottom: 2px solid darkgray;">
                    <td style="border-bottom: none; background-color: #379fc5e7;">
                        <div class="attendancebox" style="display: flex; justify-content:center; border-right: none;">
                            <div style="width:30%; display: inline-block; text-align:center; font-weight:bold; padding: 7px 0px; color: white; ">상태</div>
                            <div style="width:30%; display: inline-block; text-align:center; font-weight:bold; padding: 7px 0px; color: white; ">입실</div>
                            <div class="exit" style="width:30%; display: inline-block; text-align:center; font-weight:bold; padding: 7px 0px; color: white;">퇴실</div>  
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>1</td>
                    <td ><a href="studentinfo.jsp" >홍길동</a></td>
                    <td>빅데이터</td>
                    <td>25.01.20</td>
                    <td>
                        <div class="attendancebox" style="display: flex; justify-content:center;">
                            <div style="width:30%; display: inline-block; text-align:center;">출석</div>
                            <div style="width:30%; display: inline-block; text-align:center;">9:00</div>
                            <div class="exit" style="width:30%; display: inline-block; text-align:center;">18:00</div>  
                        </div>
                    </td>
                    <td style="border-right: none;" >
                        <span>출0</span>
                        <span>지0</span>
                        <span>결0</span>
                    </td>
                </tr>
            </table>
        </div>
    </body>
</html>