<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<html>
<head>
    <title>회원 목록</title>
</head>
<body>
    <h2>회원 목록</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Password</th>
            <th>Name</th>
            <th>Email</th>
            <th>Join Date</th>
        </tr>
        <c:forEach var="member" items="${membersList}">
            <tr align="center">
                <td>${member.id}</td>
                <td>${member.pwd}</td>
                <td>${member.name}</td>
                <td>${member.email}</td>
                <td>${member.joinDate}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
