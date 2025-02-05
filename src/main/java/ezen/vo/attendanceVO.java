package ezen.vo;

//클래스명 : attendanceVO
//작성자명 : 천은정
//작성일자 : 2025.02.04
//기능설명 : 출결 정보를 관리하기 위한 클래스
public class attendanceVO {
	private String idx;			//출석관리번호
	private String checktime;	//체크시간
	private String sno ;		//학생번호
	private String classno ;	//강좌번호
	
	//setter
	public void setIdx 			(String idx) 	  	  {	this.idx = idx;				}
	public void setChecktime	(String checktime) 	  {	this.checktime = checktime;	}
	public void setSno 			(String sno) 		  {	this.sno = sno;				}
	public void setClassno 		(String classno) 	  {	this.classno = classno;		}
	
	//getter
	public String getIdx() 			{	return idx;			}
	public String getChecktime() 	{	return checktime;	}
	public String getSno() 			{	return sno;			}
	public String getClassno() 		{	return classno;		}
}
