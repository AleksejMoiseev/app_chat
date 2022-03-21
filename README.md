## app_chat aplication
gunicorn -c settings.py example:api  --reload

Аутентификация (через headrs), регистрация пользователей - реализовано 
регистрация пользователей проходит при отправке своих данных на url:


1. POST: http://127.0.0.1:8080/register
В качестве ответа приходит access token
![img.png](img/register.png)


2. Аутентификация (через headrs)

### Примеры запросов
3. POST: http://127.0.0.1:8080/chats создание чата 
создать чат может любой пользователь у которого есть access token - реализовано


![img.png](img/img1.png)


PUT, PATCH, DELETE: http://127.0.0.1:8080/chats/{chat_id}
обновить чат, удалить чат может только создатель чата

![img.png](img/putpatch.png)

4. GET: http://127.0.0.1:8080/info/0

получить информацию о чате
Любой участник чата

![img.png](img/info.png)

5. POST: http://127.0.0.1:8080/members

Добавить пользователя в чат

![img.png](img/add_member.png)

6. DELETE http://127.0.0.1:8080/members

Выгнать пользователя из чата

![img.png](img/del_member.png)


пользователь не имеет более доступа к ресурсам чата


![img.png](img/result.png)



7. http://127.0.0.1:8080/members/0
Получить всех участников чата, может владелец чата и участник

![img.png](img/get_members.png)


8. POST: http://127.0.0.1:8080/messages отправка сообщения в чат
отправить сообщение в чат может владелец чата - реализовано
отправить сообщение может участник  - реализовано

![img.png](img/send.png)

GET: http://127.0.0.1:8080/messages/0

9. Получать все сообщения чата, получить может владелец чата
и участник чата - реализовано

![img.png](img/get_messages.png)
