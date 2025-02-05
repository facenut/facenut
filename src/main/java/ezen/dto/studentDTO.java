package ezen.dto;

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
		
		String sql = "";
		sql += "insert into studentinfo (sname, classno, birthday, phone) ";
		sql += "values(";
		sql += "'" + _R(vo.getSname())	  + "',";
		sql += "'" + _R(vo.getClassno())  + "',";
		sql += "'" + _R(vo.getBirthday()) + "',";
		sql += "'" + _R(vo.getPhone())	  + "'";
		sql += ")";
		this.execute(sql);
		
		this.dbDisconnect();
		return true;	
	}
	
	//회원정보 수정 처리
	//리턴값 : true 이면 정보 변경, false 이면 변경 실패
	public boolean Changeinfo(String sno, String sname, String phone)
	{
		this.driverLoad();
		this.dbConnect();
		
		String sql = "";
		sql += "update user ";
		sql += "set sname = '" + sname + "' ";
		sql += "set phone = '" + phone + "' ";
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
		sql += "select sname,classno,birthday,phone, ";
		sql += "from studentinfoVO ";
		sql += "where sno = " + sno;
		
		this.executeQuery(sql);
		this.next();
		
		studentinfoVO vo = new studentinfoVO();
		vo.setSname	(this.getString("sname"));
		vo.setClassno		(this.getString("classno"));
		vo.setBirthday	(this.getString("birthday"));
		vo.setPhone	(this.getString("phone"));
		
		this.dbDisconnect();
		return vo;
	}
	
	// 학생 데이터의 전체 갯수를 얻는다.
	// classno: 구분(1=빅데이터, 2=웹디자인, 3=AWS)
	// 리턴값 : 학생정보의 갯수
	public int GetTotal(String classno) {
		driverLoad();
		dbConnect();
		
		String sql = "";
		sql += "select count(*) as total ";
		sql += "from studentinfoVO ";
		sql += "where classno = '" + classno + "' and bigdata = '1', webdesign = '2', AWS = '3'";
		executeQuery(sql);
		int total = this.getInt("total");
		
		dbDisconnect();
		return total;
	}
}
