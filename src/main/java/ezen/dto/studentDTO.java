package ezen.dto;

import java.sql.PreparedStatement;
import java.util.ArrayList;

import ezen.dao.DBManager;
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
		sql += "update user ";
		sql += "set sname = '" + sname + "' ";
		sql += "set phone = '" + phone + "' ";
		sql += "set classno = '" + classno + "' ";
		sql += "where sno = '" + sno + "' ";
		this.execute(sql);
		this.dbDisconnect();
		
		return true;
	}
		
	//회원정보 조회	
	public studentinfoVO read(String sno) {
		this.driverLoad();
		this.dbConnect();
		
		String sql  = "";
		sql += "select sname, classno, birthday, phone ";
		sql += "from studentinfoVO ";
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
	// 리턴값 : 학생정보의 갯수
	public studentinfoVO updateStatus (String sno,String status) {
	    this.driverLoad();
	    this.dbConnect();
	    
	    String sql  = "";
	    sql += "select sno, sname, classno, birthday, phone, status ";  // status 추가
	    sql += "from studentinfo ";
	    sql += "where sno = " + sno;  // 현재 형태 그대로 진행
	    System.out.println(sql);
	    this.executeQuery(sql);
	    this.next();
	    
	    studentinfoVO vo = new studentinfoVO();
	    vo.setSno   (this.getString("sno"));
	    vo.setSname   (this.getString("sname"));
	    vo.setClassno (this.getString("classno"));
	    vo.setBirthday(this.getString("birthday"));
	    vo.setPhone   (this.getString("phone"));
	    vo.setStatus  (this.getString("status"));  // status 값도 가져오기
	    
	    this.dbDisconnect();
	    return vo;
	}




	// 학생 데이터의 전체 갯수를 얻는다.
	// classno: 구분(1=빅데이터, 2=웹디자인, 3=AWS)
	// 리턴값 : 학생정보의 갯수
	public int GetTotal(String status) {
		driverLoad();
		dbConnect();
		
		String sql = "";
		sql += "select count(*) as total ";
		sql += "from studentinfoVO ";
		sql += "where status = '" + status + "' and approve = '1'";
		executeQuery(sql);
		int total = this.getInt("total");
		
		dbDisconnect();
		return total;
	}
	
	// 학생 목록 조회 : 목록을 ArrayList 변수 list 에 최신순으로 저장
	public ArrayList<studentinfoVO> GetList(String sno, int pageno, String status) {
		
		ArrayList<studentinfoVO> list = new ArrayList<studentinfoVO>();
		
		//int startno = (pageno - 1) * 10;
		
		this.driverLoad();
		this.dbConnect();
		
		String sql = "";
		sql += "select no, title, wdate, userid, hit, isguest, deleted, ";
		sql += "(select usernick from user where userid = board.userid) as usernick, ";
		sql += "(select count(*) from reply where no = board.no and rdeleted = 0 and depth = 0) as count ";
		sql += "from board ";
		sql += "where sno = '" + sno + "' and status = '" + status + "' ";
		sql += "order by no desc ";
		//sql += "limit " + startno + "," + studentinfoVO.pageRows;
		
		executeQuery(sql);
		
		while(next()) {
			studentinfoVO vo = new studentinfoVO();
			vo.setSno		(getString("sno"));
			vo.setSname		(getString("sname"));
			vo.setClassno	(getString("classno"));
			vo.setBirthday		(getString("birthday"));
			vo.setPhone	(getString("phone"));
			vo.setStatus	(getString("status"));
		}
		
		dbDisconnect();
		return list;
	}
	
	
	 //승인여부 //0 = 대기, 1 = 승인, 2 = 삭제 //리턴값 : true 이면 승인 처리, false 이면 실패 public
	 public boolean approve(String sno,String status) { 
		 this.driverLoad(); 
		 this.dbConnect();
	 
		 String sql = ""; 
		 sql += " UPDATE studentinfo "; 
		 sql += " SET status = " + status + " ";
		 sql += " WHERE sno = '" + sno + "' ";
		 System.out.println(sql); 
		 
		 int result = this.executeUpdate(sql);
		 System.out.println(result);
		 
		 this.dbDisconnect();
		 
		 if(result == 1) {
				this.dbDisconnect();
				return true;	
			}else {
				this.dbDisconnect();
				return false;
			}
		 }
		 
	
}

