package ezen.vo;

//클래스명 : studentVO
//작성자명 : 천은정
//작성일자 : 2025.02.04
//기능설명 : 학생 정보를 관리하기 위한 클래스
public class studentinfoVO {
	private String sno;			//학생등록번호
	private String sname;		//학생이름
	private String classno;		//강좌번호
	private String birthday;	//생년월일
	private String phone;		//전화번호
	private String status;		//승인여부
	
	
	//setter
	public void setSno 		(String sno) 	  {	this.sno = sno;				}
	public void setSname 	(String sname) 	  {	this.sname = sname;			}
	public void setClassno 	(String classno)  {	this.classno = classno;		}
	public void setBirthday (String birthday) {	this.birthday = birthday;	}
	public void setPhone 	(String phone) 	  {	this.phone = phone;		 	}
	public void setStatus 	(String status)   {	this.status = status;	 	}
	
	//getter
	public String getSno() 		{	return sno;		}
	public String getSname() 	{	return sname;	}
	public String getClassno() 	{	return classno;	}
	public String getBirthday() {	return birthday;}
	public String getPhone() 	{	return phone;	}
	public String getStatus() 	{	return status;	}
}
