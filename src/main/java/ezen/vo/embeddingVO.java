package ezen.vo;

//클래스명 : embeddingVO
//작성자명 : 천은정
//작성일자 : 2025.02.04
//기능설명 : 임베딩값 정보를 관리하기 위한 클래스
public class embeddingVO {
	private String idx;			//임베딩 번호
	private String embedding;	//임베딩 값
	private String sno;			//학생번호
	
	//setter
	public void setIdx 			(String idx) 	  	  {	this.idx = idx;				}
	public void setEmbedding	(String embedding) 	  {	this.embedding = embedding;	}
	public void setSno 			(String sno) 		  {	this.sno = sno;				}
		
	//getter
	public String getIdx() 			{	return idx;			}
	public String getEmbedding() 	{	return embedding;	}
	public String getSno() 			{	return sno;			}
}
