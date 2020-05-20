insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(1,datetime('now','localtime'),datetime('now','localtime'),false,'五年一贯大专','又称“初中起点大专教育”，招收参加中考的初中毕业生，达到录取成绩后，进入高等职业学校学习，进行一贯制的培养。学业期满颁发国家教育部统一印制的《普通高等学校毕业证书》，此学历为国家承认的全日制专科学历，修业年限注明“五年一贯制”字样，与三年制专科基本无异。毕业生具有继续接受本科以上教育的资格。毕业生就业在国家宏观政策指导下，实行双向选择、自主择业。',1,false,null);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(2,datetime('now','localtime'),datetime('now','localtime'),false,'中职','招生对象是初中毕业生和具有与初中同等学历的人员，基本学制为三年，学生毕业属中职学历。',1,false,null);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(3,datetime('now','localtime'),datetime('now','localtime'),false,'交通','高等职业学校专业教学标准：交通运输大类',2,false,1);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(4,datetime('now','localtime'),datetime('now','localtime'),false,'交通','中等职业学校专业教学标准：交通运输类',2,false,2);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(5,datetime('now','localtime'),datetime('now','localtime'),false,'计算机','高等职业学校专业教学标准：电子信息大类',2,false,1);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(6,datetime('now','localtime'),datetime('now','localtime'),false,'计算机','中等职业学校专业教学标准：电子信息类',2,false,2);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(7,datetime('now','localtime'),datetime('now','localtime'),false,'财经','高等职业学校专业教学标准：财经商贸大类',2,false,1);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(8,datetime('now','localtime'),datetime('now','localtime'),false,'财经','中等职业学校专业教学标准：财经商贸类',2,false,2);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(9,datetime('now','localtime'),datetime('now','localtime'),false,'艺术','高等职业学校专业教学标准：文化艺术大类',2,false,1);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(10,datetime('now','localtime'),datetime('now','localtime'),false,'艺术','中等职业学校专业教学标准：文化艺术类',2,false,2);
insert into tb_major_category(id,create_time,update_time,is_delete,name,desc,category_type, is_tab, parent_category_id) 
                          values(11,datetime('now','localtime'),datetime('now','localtime'),false,'烹饪','中等职业学校专业教学标准：旅游服务类',2,false,2);