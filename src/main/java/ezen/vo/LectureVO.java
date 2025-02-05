package ezen.vo;

public class LectureVO
{
    private String classno;     //강좌번호
    private String classroom;   //강의실
    private String begin_hour;  //강의 시작시간
    private String end_hour;    //강의 종료시간
    private String begin_date;  //강시 시작날짜
    private String end_date;    //강의 종료날짜

    public void setClassno	    (String classno)	{ this.classno	    = classno;	    }
	public void setClassroom	(String classroom)	{ this.classroom 	= classroom;    }
	public void setBegin_hour   (String begin_hour)	{ this.begin_hour   = begin_hour;	}
	public void setEnd_hour	    (String end_hour)   { this.end_hour 	= end_hour;	    }
	public void setBegin_date	(String begin_date)	{ this.begin_date   = begin_date;   }
    public void setEnd_date 	(String end_date)	{ this.end_date     = end_date;     }

    public String getClassno()		{ return classno;	    }
	public String getClassroom()	{ return classroom;	    }
	public String getBegin_hour ()	{ return begin_hour;	}
	public String getEnd_hour()	    { return end_hour;		}
	public String getBegin_date()	{ return begin_date; 	}
    public String getEnd_date()	    { return end_date; 	    }
}