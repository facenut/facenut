package ezen.dto;

import java.sql.PreparedStatement;
import java.util.ArrayList;

import ezen.dao.DBManager;
import ezen.vo.attendanceVO;
import ezen.vo.studentinfoVO;

//클래스명 : studentDTO
//작성자명 : 천은정
//작성일자 : 2025.02.04
//기능설명 : studentinfoVO의 정보를 관리하기 위한 클래스
public class studentDTO extends DBManager {

	//회원가입
	public boolean join(studentinfoVO vo) {
		this.driverLoad();
		this.dbConnect();
		System.out.println(vo.getSname());
		System.out.println(vo.getClassno());
		System.out.println(vo.getBirthday());
		System.out.println(vo.getPhone());
		String sql = "";
		sql += "insert into studentinfo (sname, classno, birthday, phone) ";
		sql += "values(";
		sql += "'" + _R(vo.getSname())	  + "', ";
		sql += " " + _R(vo.getClassno())  + ", ";
		sql += "'" + _R(vo.getBirthday()) + "', ";
		sql += "'" + _R(vo.getPhone())	  + "' ";
		sql += ")";
		int result = this.executeUpdate(sql);
		if(result > 0) {
			this.dbDisconnect();
			return true;	
		}else {
			this.dbDisconnect();
			return false;
		}
	}
	
	//회원정보 수정 처리
	//리턴값 : true 이면 정보 변경, false 이면 변경 실패
	public boolean Changeinfo(String sno, String sname, String phone, String classno)
	{
		this.driverLoad();
		this.dbConnect();
		
		String sql = "";
		sql += "update studentinfo ";
		sql += "set sname = '" + sname + "', ";
		sql += "phone = '" + phone + "', ";
		sql += "classno = '" + classno + "' ";
		sql += "where sno = '" + sno + "' ";
		this.execute(sql);
		System.out.println(sql);
		this.dbDisconnect();
		
		return true;
	}
		
	//회원정보 조회	
	public studentinfoVO read(String sno) {
		this.driverLoad();
		this.dbConnect();
		
		String sql  = "";
		sql += "select sname, classno, birthday, phone ";
		sql += "from studentinfo ";
		sql += "where sno = " + sno;
		
		this.executeQuery(sql);
		this.next();
		
		studentinfoVO vo = new studentinfoVO();
		vo.setSname	  	(this.getString("sname"));
		vo.setClassno 	(this.getString("classno"));
		vo.setBirthday 	(this.getString("birthday"));
		vo.setPhone		(this.getString("phone"));
		vo.setStatus	(this.getString("status"));
		
		this.dbDisconnect();
		return vo;
	}
	
	// 승인대기 학생 목록
	// status: 구분(0=대기, 1=승인, 2=삭제)
	// 리턴값 : 미승인 학생목록과 정보
//	public studentinfoVO notApproved() {
//	    this.driverLoad();
//	    this.dbConnect();
//	    
//	    String sql  = "";
//	    sql += "select sno, sname, classno, birthday, phone, status ";  // status 추가
//	    sql += "from studentinfo ";
//	    sql += "where status = 0";
//	    System.out.println(sql);
//	    this.executeQuery(sql);
//	    this.next();
//	    
//	    studentinfoVO vo = new studentinfoVO();
//	    vo.setSno   (this.getString("sno"));
//	    vo.setSname   (this.getString("sname"));
//	    vo.setClassno (this.getString("classno"));
//	    vo.setBirthday(this.getString("birthday"));
//	    vo.setPhone   (this.getString("phone"));
//	    vo.setStatus  (this.getString("status"));  // status 값도 가져오기
//	    
//	    this.dbDisconnect();
//	    return vo;
//	}




	// 학생 데이터의 전체 갯수를 얻는다.
	// classno: 구분(1=빅데이터, 2=웹디자인, 3=AWS)
	// 리턴값 : 학생정보의 갯수
	public int GetTotal(String status) {
		driverLoad();
		dbConnect();
		
		String sql = "";
		sql += "select count(*) as total ";
		sql += "from studentinfo ";
		sql += "where status = 1";
		executeQuery(sql);
		int total = this.getInt("total");
		
		dbDisconnect();
		return total;
	}
	
	// 학생 목록 조회
	public ArrayList<studentinfoVO> GetList(String status) {
		
		ArrayList<studentinfoVO> list = new ArrayList<studentinfoVO>();
		
		//int startno = (pageno - 1) * 10;
		
		this.driverLoad();
		this.dbConnect();
		
		String sql = "";
		sql += "select sno, sname, classno, birthday, phone, status ";
		sql += "from studentinfo ";
		sql += "where status = " + status;
		
		System.out.println(sql);
		
		executeQuery(sql);
		
		while(next()) {
			studentinfoVO vo = new studentinfoVO();
			vo.setSno		(getString("sno"));
			vo.setSname		(getString("sname"));
			vo.setClassno	(getString("classno"));
			vo.setBirthday	(getString("birthday"));
			vo.setPhone		(getString("phone"));
			vo.setStatus	(getString("status"));
			list.add(vo);
		}
		
		dbDisconnect();
		return list;
	}
	
	// 일별 출석 현황 조회
	public ArrayList<attendanceVO> GetAttendList(String date) {
		
		ArrayList<attendanceVO> list = new ArrayList<attendanceVO>();
		
		this.driverLoad();
		this.dbConnect();
		
	/*	String sql = "";
		sql += "SELECT a.sno, s.sname, a.classno, MIN(a.checktime) as checkin, MAX(a.checktime) as checkout, COUNT(a.checktime) as count ";
		sql += "FROM attendance a ";
		sql += "JOIN studentinfo s ON a.sno = s.sno ";
		sql += "WHERE DATE(a.checktime) = '" + date + "' ";
		sql += "GROUP BY a.sno, s.sname, a.classno ";
		sql += "ORDER BY checkin ASC";	*/
		
		String sql = "";
		sql += "SELECT a.sno, s.sname, a.classno, a.checktime, a.event ";
		sql += "FROM attendance a ";
		sql += "JOIN studentinfo s ON a.sno = s.sno ";
		sql += "WHERE DATE(a.checktime) = '" + date + "' ";
		sql += "ORDER BY sno, checktime ASC";
		
		System.out.println(sql);
		
		executeQuery(sql);
		/*
		//ArrayList<String> events = new ArrayList<>();
		attendanceVO vo = new attendanceVO(); 
				if(next()) {
			System.out.println("조회된 데이터가 있음");
			while(true) {
				if(!getString("sno").equals(vo.getSno())) {
					System.out.println("가져온 데이터가 기존 데이터와 다름");
					if(vo.getSno() != null) {
						System.out.println("기존 데이터가 있음");
						vo.setEvents(events);
						System.out.println("리스트에 vo를 넣음");
						list.add(vo);
					}else {
						System.out.println("기존 데이터가 없음");
						// 새로운 vo를 만들어 정보를 저장
						vo = new attendanceVO();
						events = new ArrayList<>();
						vo.setSno		(getString("sno"));
						vo.setSname		(getString("sname"));
						vo.setClassno	(getString("classno"));
						vo.setCheckin	(getString("checktime"));
						vo.setCheckin	(getString("checktime"));
					}
				}else
				{	// 같으면 추가 정보만 넣음
					System.out.println("가져온 데이터가 기존 vo와 이름이 같음");
					vo.setCheckout	(getString("checktime"));
				}
				System.out.println(vo.getSname() + " : " + getString("event"));
				events.add(getString("event"));
				
				if(!next()) {
					// 다음 데이터가 없음
					vo.setEvents(events);
					list.add(vo);
					break;
				}
			}
		}
		 
		*/
		while(next()) {
			attendanceVO vo = new attendanceVO();
			vo.setSno		(getString("sno"));
			vo.setSname		(getString("sname"));
			vo.setClassno	(getString("classno"));
			vo.setCheckin	(getString("checktime"));
			vo.setCheckout	(getString("checktime"));
			vo.setChecktime	(getString("checktime"));
			vo.setEvent		(getString("event"));
			System.out.println(getString("event"));
			list.add(vo);
		}
		
		dbDisconnect();
		return list;
	}
	
	
	 //승인여부 //0 = 대기, 1 = 승인, 2 = 삭제 //리턴값 : true 이면 승인 처리, false 이면 실패
	 public boolean approve(String sno,String status) { 
		 this.driverLoad(); 
		 this.dbConnect();
	 
		 String sql = ""; 
		 sql += " UPDATE studentinfo "; 
		 sql += " SET status = " + status + " ";
		 sql += " WHERE sno = " + sno;
		 System.out.println(sql); 
		 
		 int result = this.executeUpdate(sql);
		 System.out.println(result);
		 
		 this.dbDisconnect();
		 
		 if( result == 1 ) {
				this.dbDisconnect();
				return true;	
			}else {
				this.dbDisconnect();
				return false;
			}
		 }
	 
			/*
			 * public ArrayList<attendanceVO> GetList() {
			 * 
			 * ArrayList<attendanceVO> list = new ArrayList<attendanceVO>();
			 * 
			 * //int startno = (pageno - 1) * 10;
			 * 
			 * this.driverLoad(); this.dbConnect();
			 * 
			 * String sql = ""; sql += "select idx, checktime, attendate, sno, classno ";
			 * sql += "from studentinfo ";
			 * 
			 * System.out.println(sql);
			 * 
			 * executeQuery(sql);
			 * 
			 * while(next()) { attendanceVO vo = new attendanceVO(); vo.setIdx
			 * (getString("idx")); vo.setChecktime (getString("checktime")); vo.setAttendate
			 * (getString("attendate")); vo.setSno (getString("sno")); vo.setClassno
			 * (getString("classno")); list.add(vo); }
			 * 
			 * dbDisconnect(); return list;
			 * 
			 * }
			 */
}
