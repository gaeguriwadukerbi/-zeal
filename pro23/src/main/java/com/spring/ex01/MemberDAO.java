package com.spring.ex01;

import java.io.Reader;
import java.util.List;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class MemberDAO {
    private static SqlSessionFactory sqlMapper = null;

    // SqlSessionFactory 인스턴스를 얻기 위한 메서드
    public static SqlSessionFactory getInstance() {
        if (sqlMapper == null) {
            try {
                String resource = "mybatis/SqlMapConfig.xml";
                Reader reader = Resources.getResourceAsReader(resource);
                sqlMapper = new SqlSessionFactoryBuilder().build(reader);
                reader.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sqlMapper;
    }

    // 모든 회원 정보를 조회하는 메서드
    public List<MemberVO> selectAllMemberList() {
        sqlMapper = getInstance();
        SqlSession session = sqlMapper.openSession();
        List<MemberVO> memlist = null;
        try {
            memlist = session.selectList("mapper.member.selectAllMemberList");
        } finally {
            session.close();
        }
        return memlist;
    }
}
