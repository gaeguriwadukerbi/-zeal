<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%
    request.setCharacterEncoding("UTF-8");
%>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원 정보 출력창</title>
    <style>
        .cls1 { font-size: 40px; text-align: center; }
        .table-center { margin: 0 auto; }
    </style>
</head>
<body>
    <c:choose>
        <c:when test="${msg == 'addMember'}">
            <script>
                window.onload = function() {
                    alert("회원이 등록되었습니다.");
                }
            </script>
        </c:when>
        <c:when test="${msg == 'modified'}">
            <script>
                window.onload = function() {
                    alert("회원의 정보를 수정했습니다.");
                }
            </script>
        </c:when>
        <c:when test="${msg == 'deleted'}">
            <script>
                window.onload = function() {
                    alert("회원의 정보를 삭제했습니다.");
                }
            </script>
        </c:when>
    </c:choose>
    <table class="table-center">
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
                <tr style="text-align: center;">
                    <td>${mem.id}</td>
                    <td>${mem.pwd}</td>
                    <td>${mem.name}</td>
                    <td>${mem.email}</td>
                    <td>${mem.joinDate}</td>
                    <td><a href="${contextPath}/member/modMemberForm.do?id=${mem.id}">수정</a></td>
                    <td><a href="${contextPath}/member/delMember.do?id=${mem.id}">삭제</a></td>
                </tr>
            </c:forEach>
        </c:when>
    </c:choose>
    </table>
</body>
</html>
