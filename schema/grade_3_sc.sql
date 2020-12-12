CREATE TABLE IF NOT EXISTS sc  (
    stu_sn     INTEGER,     --学号
    cou_sn     INTEGER,     -- 课程序号
    state   TEXT,

    PRIMARY KEY(stu_sn, cou_sn)
);

ALTER TABLE sc 
    ADD CONSTRAINT stu_sn_fk FOREIGN KEY (stu_sn) REFERENCES student(sn);
ALTER TABLE sc
    ADD CONSTRAINT cou_sn_fk FOREIGN KEY (cou_sn) REFERENCES course(sn);