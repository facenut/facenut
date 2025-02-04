package ezen.vo;
public class FaceVO 
{
    private String face_idx;	// 얼굴 인덱스
	private String sno;	    	// 학생번호
	private String idx;	        // 관리번호
	private String pname;		// 파일이름
	private String lname;	    // 원본이름
	
    public void setFace_idx	(String face_idx)	{ this.face_idx	= face_idx;	}
	public void setSno	    (String sno)		{ this.sno	    = sno;	    }
	public void setIdx      (String idx)	    { this.idx	    = idx;	    }
	public void setPname	(String pname)		{ this.pname	= pname;	}
	public void setLname	(String lname)	    { this.lname    = lname;	}

    public String getFace_idx()		{ return face_idx;	}
	public String getSno()	        { return sno;	    }
	public String getIdx ()	        { return idx;	    }
	public String getPname()	    { return pname;		}
	public String getLname()	    { return lname; 	}
}





