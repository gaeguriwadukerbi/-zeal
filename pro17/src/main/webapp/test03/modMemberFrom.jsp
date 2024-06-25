<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%
    request.setCharacterEncoding("UTF-8");
%>
<%
    String contextPath = request.getContextPath();
%>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원 정보 수정창</title>
    <style>
        .right-align { text-align: right; }
        .center-table { margin: 0 auto; }
    </style>
</head>
<body>
    <h1 class="cls1">회원 정보 수정창</h1>
    <form method="post" action="${contextPath}/member/modMember.do?id=${memInfo.id}">
        <table class="center-table">
            <tr>
                <td width="200" class="right-align">
                    <p>아이디</p>
                </td>
                <td width="400">
                    <input type="text" name="id" value="${memInfo.id}" disabled>
                </td>
            </tr>
            <tr>
                <td width="200" class="right-align">
                    <p>비밀번호</p>
                </td>
                <td width="400">
                    <input type="password" name="pwd" value="${memInfo.pwd}">
                </td>
            </tr>
            <tr>
                <td width="200" class="right-align">
                    <p>이름</p>
                </td>
                <td width="400">
                    <input type="text" name="name" value="${memInfo.name}">
                </td>
            </tr>
            <tr>
                <td width="200" class="right-align">
                    <p>이메일</p>
                </td>
                <td width="400">
                    <input type="text" name="email" value="${memInfo.email}">
                </td>
            </tr>
            <tr>
                <td colspan="2" style="text-align: center;">
                    <input type="submit" value="수정하기">
                </td>
            </tr>
        </table>
    </form>
</body>
</html>
