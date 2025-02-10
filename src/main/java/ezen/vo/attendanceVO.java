package ezen.vo;

import java.util.ArrayList;

//클래스명 : attendanceVO
//작성자명 : 천은정
//작성일자 : 2025.02.04
//기능설명 : 출결 정보를 관리하기 위한 클래스
public class attendanceVO {
	private String idx;			//출석관리번호
	private String checktime;	//체크시간
	private String checkin;		//출석시간
	private String checkout;	//퇴실시간
	private String sno ;		//학생번호
	private String sname;		//학생이름
	private String classno ;	//강좌번호
	private String count;		//체크횟수
	private String event;
	private ArrayList<String> events;
	
	//setter
	public void setIdx 			(String idx) 	  	  {	this.idx = idx;				}
	public void setChecktime	(String checktime) 	  {	this.checktime = checktime;	}
	public void setCheckin		(String checkin) 	  {	this.checkin   = checkin;	}
	public void setCheckout		(String checkout) 	  {	this.checkout  = checkout;	}
	public void setSno 			(String sno) 		  {	this.sno = sno;				}
	public void setSname		(String sname) 		  {	this.sname = sname;			}
	public void setClassno 		(String classno) 	  {	this.classno = classno;		}
	public void setCount 		(String count) 		  {	this.count = count;			}
	public void setEvent 		(String event) 		  {	this.event = event;			}
	
	//getter
	public String getIdx() 			{	return idx;			}
	public String getChecktime() 	{	return checktime;	}
	public String getCheckin()		{	return checkin;		}
	public String getCheckout() 	{	return checkout;	}
	public String getSno() 			{	return sno;			}
	public String getSname() 		{	return sname;		}
	public String getClassno() 		{	return classno;		}
	public String getCount() 		{	return count;		}
	public String getEvent() 		{	return event;		}
	
	
	public ArrayList<String> getEvents() {
		return events;
	}
	public void setEvents(ArrayList<String> events) {
		this.events = events;
	}
	
	@Override
	public String toString() {
		return "attendanceVO [idx=" + idx + ", checktime=" + checktime + ", checkin=" + checkin + ", checkout="
				+ checkout + ", sno=" + sno + ", sname=" + sname + ", classno=" + classno + ", count=" + count
				+ ", event=" + event + ", events=" + events + ", getIdx()=" + getIdx() + ", getChecktime()="
				+ getChecktime() + ", getCheckin()=" + getCheckin() + ", getCheckout()=" + getCheckout() + ", getSno()="
				+ getSno() + ", getSname()=" + getSname() + ", getClassno()=" + getClassno() + ", getCount()="
				+ getCount() + ", getEvent()=" + getEvent() + ", getEvents()=" + getEvents() + ", getClass()="
				+ getClass() + ", hashCode()=" + hashCode() + ", toString()=" + super.toString() + "]";
	}
}