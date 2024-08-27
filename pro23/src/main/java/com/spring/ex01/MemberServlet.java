package com.spring.ex01;

import java.io.IOException;
import java.util.List;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/mem.do")
public class MemberServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doHandle(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doHandle(request, response);
    }

    private void doHandle(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/html;charset=utf-8");

        // MemberDAO 객체 생성
        MemberDAO dao = new MemberDAO();

        // DAO의 selectAllMemberList 메서드를 호출하여 회원 목록을 가져옴
        List membersList = dao.selectAllMemberList();

        // request 객체에 회원 목록을 속성으로 설정
        request.setAttribute("membersList", membersList);

        // 회원 목록을 출력할 JSP 페이지로 포워딩
        RequestDispatcher dispatch = request.getRequestDispatcher("test01/listMembers.jsp");
        dispatch.forward(request, response);
    }
}
