<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" isELIgnored="false"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<c:set var="contextPath" value="${pageContext.request.contextPath}" />

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>게시판</title>
    <style>
        .cls1 {
            text-decoration: none;
        }
        .cls2 {
            text-align: center;
            font-size: 30px;
        }
    </style>
</head>
<body>
    <c:choose>
        <c:when test="${articlesList == null}">
            <tr height="10">
                <td colspan="4">
                    <p align="center">
                        <b><span style="font-size:9pt;">등록된 글이 없습니다.</span></b>
                    </p>
                </td>
            </tr>
        </c:when>
        <c:when test="${articlesList != null}">
            <c:forEach var="article" items="${articlesList}" varStatus="articleNum">
                <tr align="center">
                    <td width="5%">${articleNum.count}</td>
                    <td width="10%">${article.id }</td>
                    <td align="left" width="35%">
                        <span style="padding-right:30px"></span>
                        <c:choose>
                            <c:when test="${article.level > 1}">
                                <c:forEach begin="1" end="${article.level}" step="1">
                                    <span style="padding-left:20px"></span>
                                </c:forEach>
                                <span style="font-size:12px;">답변</span>
                                <a class="cls1" href="${contextPath}/board/viewArticle.do?articleNO=${article.articleNO}">
                                    articleNO=${article.articleNO}${article.title}
                                </a>
                            </c:when>
                            <c:otherwise>
                                <a class="cls1" href="${contextPath}/board/viewArticle.do?articleNO=${article.articleNO}">
                                    articleNO=${article.articleNO}${article.title}
                                </a>
                            </c:otherwise>
                        </c:choose>
                    </td>
                    <td width="10%">
                        <fmt:formatDate value="${article.writeDate}" />
                    </td>
                </tr>
            </c:forEach>
        </c:when>
    </c:choose>
</body>
</html>
