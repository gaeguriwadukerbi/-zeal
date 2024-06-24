package sec02.ex02;

import java.sql.Connection;
import java.sql.PreparedStatement;
import javax.sql.DataSource;
import javax.naming.Context;
import javax.naming.InitialContext;

public class MemberDAO {
    private DataSource dataFactory;
    private Connection conn;
    private PreparedStatement pstmt;

    public MemberDAO() {
        try {
            Context ctx = new InitialContext();
            Context envContext = (Context) ctx.lookup("java:/comp/env");
            dataFactory = (DataSource) envContext.lookup("jdbc/oracle");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public MemberVO findMember(String _id) {
        MemberVO memInfo = null;
        try {
            conn = dataFactory.getConnection();
            String query = "select * from t_member where id=?";
            System.out.println(query);
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, _id);
            ResultSet rs = pstmt.executeQuery();
            rs.next();
            String id = rs.getString("id");
            String pwd = rs.getString("pwd");
            String name = rs.getString("name");
            String email = rs.getString("email");
            Date joinDate = rs.getDate("joinDate");
            memInfo = new MemberVO(id, pwd, name, email, joinDate);
            pstmt.close();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return memInfo;
    }

    public void modMember(MemberVO memberVO) {
        try {
            conn = dataFactory.getConnection();
            String id = memberVO.getId();
            String pwd = memberVO.getPwd();
            String name = memberVO.getName();
            String email = memberVO.getEmail();
            String query = "update t_member set pwd=?,name=?,email=? where id=?";
            System.out.println(query);
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, pwd);
            pstmt.setString(2, name);
            pstmt.setString(3, email);
            pstmt.setString(4, id);
            pstmt.executeUpdate();
            pstmt.close();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void delMember(String id) {
        try {
            conn = dataFactory.getConnection();
            String query = "delete from t_member where id=?";
            System.out.println(query);
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, id);
            pstmt.executeUpdate();
            pstmt.close();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
