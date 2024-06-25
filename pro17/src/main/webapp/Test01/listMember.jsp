<%@ page language="java" contentType="text/html; charset=UTF-8"
    import="java.util.*,sec01.ex01.*"
    pageEncoding="UTF-8"%>
<%@ isELIgnored="false"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%
    request.setCharacterEncoding("utf-8");
%>
<html>
<head>
<meta charset="UTF-8">
<title>회원 정보 출력 화면</title>
<style>
.cls1 {
    font-size: 40px;
    text-align: center;
}
table {
    border-collapse: collapse;
    width: 80%;
    margin: auto;
    text-align: center;
}
th, td {
    border: 1px solid #000;
    padding: 8px;
}
th {
    background-color: #4CAF50;
    color: white;
}
tr:nth-child(even) {
    background-color: #f2f2f2;
}
</style>
</head>
<body>
    <h1 align="center">회원정보</h1>
    <table>
        <tr>
            <th>아이디</th>
            <th>비밀번호</th>
            <th>이름</th>
            <th>이메일</th>
            <th>가입일</th>
        </tr>
        <c:choose>
            <c:when test="${membersList == null}">
                <tr>
                    <td colspan="5">
                        <b>등록된 회원이 없습니다.</b>
                    </td>
                </tr>
            </c:when>
            <c:when test="${membersList != null}">
                <c:forEach var="mem" items="${membersList}">
                    <tr>
                        <td>${mem.id }</td>
                        <td>${mem.pwd }</td>
                        <td>${mem.name }</td>
                        <td>${mem.email }</td>
                        <td><fmt:formatDate value="${mem.joinDate}" pattern="yyyy-MM-dd"/></td>
                    </tr>
                </c:forEach>
            </c:when>
        </c:choose>
    </table>
    <p class="cls1"><a href="#">회원 가입하기</a></p>
</body>
</html>
