import allure

def attach_reqres(response):
    request = response.request

    allure.attach(request.method, name='Метод Запроса',
                  attachment_type=allure.attachment_type.TEXT)

    allure.attach(request.url, name='URL Запроса',
                  attachment_type=allure.attachment_type.TEXT)
    
    if request.body:
        allure.attach(response.request.body, name='Тело Запроса',
                  attachment_type=allure.attachment_type.JSON)
        
    try:
        allure.attach(response.json(),name="Тело ответа",
                      attachment_type=allure.attachment_type.JSON)
    except:
        allure.attach(response.text, name="Тело ответа (text)",
                      attachment_type=allure.attachment_type.TEXT)
          
    allure.attach(str(response.status_code), name='Статус-код ответа',
                  attachment_type=allure.attachment_type.TEXT)
    

