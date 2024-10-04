package kopo.aisw.mypro.board;

import java.sql.Date;

public class BoardVO {
    // 게시판 필드
    public int bID;
    public String bTitle;
    public String bContent;
    public Date bWriteDate;

    // Getter & Setter
    public int getbID() {
        return bID;
    }

    public void setbID(int bID) {
        this.bID = bID;
    }

    public String getbTitle() {
        return bTitle;
    }
}
