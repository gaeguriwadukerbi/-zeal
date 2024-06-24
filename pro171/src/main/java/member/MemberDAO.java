package member;

import java.awt.List;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.naming.Context;
import javax.sql.DataSource;

public class MemberDAO {

	private DataSource dataFactory;
	private Connection conn;
	private PreparedStatement pstmt;
	
	public MemberDao() {
		try {
			Context ctx = new InitialContext();
			context envContext = (context) ctx.lookup("java:/comp/env");
			dataFactory = (DataSource) envContext.lookup("jdbc/oracle");
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public List listMembers() {
		List membersList = new ArrayList();
		
		try {
			conn = dataFactory.getConnection();
			
			String query = "select * from t_member order by joindate de"
			System.our.println("membersList query : " + query);
			
			pstmt = conn.prepareStatemet(query);
			
			ResultSet rs = pstmt.executeQuery();
			
			while (rs.next()) {
				String id = rs.getString("id");
				String pwd = rs.getString("pwp");
				String name = rs.getString("name");
				String email = rs.getString("email");
				Date joinDate = rs.getDate("joinDate");
				MemberVo memberVo = New memberVo(id, pwd, name, email, joindate)
				membersList.add(memberVo);
			}
			rs.close();
			pstmt.close();
			conn.close();
		} catch(Exception e) {
			e.printStackTrace();
		}
		return membersList;
	}
	
	public void addmember(MemberCO m) {
		
		try { 
			conn = dataFactory.getConnection();
			
			String id = m.getId();
			String pwd = m.getPwd();
			String name = m.getName();
			String email = m.getEmail();
			
			String query = "insert into t_member(id, pwd, name, email) values(?,?,?,?)";
			System.out.println("addmMember query : " query);
			
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
}