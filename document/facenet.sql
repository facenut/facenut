drop database facenutdb;
create database facenutdb;
use facenutdb;

create table lecture
(
classno int auto_increment primary key comment '강좌번호',
classroom int comment '강의실',
begin_hour varchar(8) comment '강의 시작시간',
end_hour varchar(8) comment '강의 종료시간',
begin_date datetime comment '강의 시작날짜',
end_date datetime comment '강의 종료날짜'
);

create table studentinfo
(
sno int auto_increment primary key comment '학생등록번호',
sname varchar(255) comment '이름',
classno int comment '강좌번호',
birthday date comment '생년월일',
phone varchar(50) comment '전화번호',
status int default 0 comment '승인여부',
foreign key(classno) references lecture(classno)
);

create table attendance
(
idx int auto_increment primary key comment '출석관리번호',
checktime timestamp default now() comment '체크시간',
sno int comment '학생번호',
classno int comment '강좌번호',
foreign key(sno) references studentinfo(sno),
foreign key(classno) references lecture(classno) 
);

create table embedding
(
idx int auto_increment primary key comment '임베딩 번호',
embedding text comment '임베딩 값',
sno int comment '학생번호',
foreign key(sno) references studentinfo(sno)
);

create table face
(
face_idx int auto_increment primary key comment '얼굴 인덱스',
sno int comment '학생번호',
idx int comment '관리번호',
pname varchar(255) comment '파일이름',
lname varchar(255) comment '원본이름',
foreign key(sno) references studentinfo(sno),
foreign key(idx) references attendance(idx)
);
