<%--
  Created by IntelliJ IDEA.
  User: AISW-203-116
  Date: 2024-10-04
  Time: 오후 4:08
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="utf-8" isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<c:set var="contextPath" value="${pageContext.request.contextPath}"/>
<% request.setCharacterEncoding("UTF-8"); %>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Board</title>
</head>
<body>
    <table border="1" align="center" width="80%">
        <tr align="center" bgcolor="#ff7f50">
            <td><b>글번호</b></td>
            <td><b>제목</b></td>
            <td><b>내용</b></td>
            <td><b>작성일</b></td>
        </tr>
        <c:forEach var="board" items="${boardList}">
            <tr align="center" bgcolor="#ff7f50">
                <td>${board.bID}</td>
                <td>${board.bTitle}</td>
                <td>${board.bContent}</td>
                <td>${board.bWritedate}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
