package sec01.ex01;

@WebServlet("/mem.do")
public class MemberController extends HttpServlet {
    private static final long serialVersionUID = 1L;
    MemberDAO memberDAO;

    public void init() throws ServletException {
        memberDAO = new MemberDAO();
    }

    protected void doHandle(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/html;charset=utf-8");
        List membersList = memberDAO.listMembers();
        request.setAttribute("membersList", membersList);
        RequestDispatcher dispatch = request.getRequestDispatcher("/test01/listMembers.jsp");
        dispatch.forward(request, response);
    }
}
