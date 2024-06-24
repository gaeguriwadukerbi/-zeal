package sec01.ex01;

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

    public List listMembers() {
        List membersList = new ArrayList();
        try {
            conn = dataFactory.getConnection();
            String query = "select * from t_member order by joinDate desc";
            System.out.println(query);
            pstmt = conn.prepareStatement(query);
            ResultSet rs = pstmt.executeQuery(query);
            while (rs.next()) {
                String id = rs.getString("id");
                String pwd = rs.getString("pwd");
                String name = rs.getString("name");
                String email = rs.getString("email");
                Date joinDate = rs.getDate("joinDate");
                MemberVO memberVO = new MemberVO(id, pwd, name, email, joinDate);
                membersList.add(memberVO);
            }
            rs.close();
            pstmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return membersList;
    }

    public void addMember(MemberVO m) {
        try {
            conn = dataFactory.getConnection();
            String id = m.getId();
            String pwd = m.getPwd();
            String name = m.getName();
            String email = m.getEmail();
            String query = "INSERT INTO t_member(id, pwd, name, email) VALUES(?, ?, ?, ?)";
            System.out.println(query);
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, id);
            pstmt.setString(2, pwd);
            pstmt.setString(3, name);
            pstmt.setString(4, email);
            pstmt.executeUpdate();
            pstmt.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
