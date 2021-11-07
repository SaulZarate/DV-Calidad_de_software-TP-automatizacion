from selenium import webdriver
import time
from data import datos
from config import configuracion

def login(driver) -> bool:
    # Ir al sitio web
    driver.get(datos["url_login"])

    # Espero 1 segundo
    time.sleep(1)

    # Input email
    input_email = driver.find_element_by_id('user_email')
    input_email.send_keys(datos["usuario"]["email"])

    # Input password
    input_password = driver.find_element_by_id('user_password')
    input_password.send_keys(datos["usuario"]["password"])
    
    time.sleep(1)
    
    try:
        # Para aceptar las cookies
        driver.find_element_by_id('onetrust-accept-btn-handler').click()
    except:
        pass
    
    # Enviar formulario
    driver.find_element_by_id('new_user').submit()
    time.sleep(3)

    try:
        driver.find_element_by_id('log_in_menu').text
        # Si imprime esto es porque encontro encontro el enlace al login (por ende no se logeo)
        return False
    except:
        return True

    #text_title = driver.find_element_by_tag_name('h1').text
    #return "¡Vamos a empezar," in text_title or "Welcome, " in text_title

def test_login():
    driver = webdriver.Chrome(executable_path=configuracion["path_driver_chrome"])
    resultado_del_test = '\n\t'
    
    if login(driver):
        resultado_del_test += 'Resultado de test_login: Bueno'
    else:
        resultado_del_test += 'Resultado de test_login: Malo'

    print(resultado_del_test + '\n')

    # Cerrar el navegador
    driver.close()

def test_guardar_como_favorito_alojamiento():
    driver = webdriver.Chrome(executable_path=configuracion["path_driver_chrome"])
    resultado_del_test = '\n\tResultado de test_guardar_como_favorito_alojamiento: '

    if not login(driver):
        print(resultado_del_test + 'Malo. No se pudo iniciar sesion')
        return
    
    # Ir a la lista de alojamientos
    driver.get(datos["url_lista_alojamientos"])
    #driver.find_element_by_css_selector('a.dropdown_trigger').click()
    # Ir al primer alojamiento
    driver.find_element_by_css_selector('a.main-thumb.vp-card.block').click()
    time.sleep(2)

    # Cambiar a la segunda pestaña
    driver.switch_to.window(driver.window_handles[1])
    
    # Agregar a favoritos
    driver.find_element_by_id('btn_wish_list').click()
    time.sleep(1)
    # Pais del alojamiento
    pais_del_alojamiento = driver.find_element_by_xpath('//*[@id="host"]/div[1]/div/div[2]/div/div/h2/span[2]/a[2]').text
    # Titulo del alojamiento
    titulo_del_alojamiento = driver.find_element_by_tag_name('h1').text

    # Ir a la página de lista de favoritos
    driver.find_element_by_class_name('tooltip-trigger').click()
    
    # div lista de paises
    div_paises = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div')
    lista_de_paises = div_paises.find_elements_by_tag_name('div')

    pais_encontrado = False
    for pais in lista_de_paises:
        if pais.find_element_by_css_selector('a h4').text == pais_del_alojamiento:
            pais_encontrado = pais
            break
    
    # Verifico que el pais del alojamiento esta en la lista
    if not pais_encontrado:
        print(resultado_del_test + 'Malo. No se encontro el pais en la lista de favoritos')
        return

    # Ir a la lista del pais
    pais_encontrado.find_element_by_tag_name('h4').click()

    # Lista de alojamientos favoritos del pais
    lista_alojamientos = driver.find_elements_by_css_selector('h2.h5.mg_bot_5')

    alojamiento_encontrado = False
    for alojamiento in lista_alojamientos:
        if alojamiento.text == titulo_del_alojamiento:
            alojamiento_encontrado = alojamiento
            break

    # Verifico si encontro el alojamiento
    if not alojamiento_encontrado:
        print(resultado_del_test + 'Malo. No se encontro el alojamiento en la lista de su pais')
        return

    # En este punto el test fue finalizado correctamente.
    # Ahora saco el alojamiento de la lista de favoritos para 
    # poder realizar las prueba cuantas veces lo desee.

    # Voy al detalle del alojamiento
    alojamiento_encontrado.click()

    # Cambiar a la tercer pestaña
    driver.switch_to.window(driver.window_handles[2])

    try:
        # "Delikeo" el alojamiento
        driver.find_element_by_id('btn_un_wish_list').click()
        print(resultado_del_test + 'Bueno')
    except:
        print(resultado_del_test + 'Bueno. Pero no se pudo sacar el alojamiento de la lista de favoritos para realizar la prueba nuevamente')
        return
    
    time.sleep(1)
    # Cierro la ventana
    driver.close()

test_login()
test_guardar_como_favorito_alojamiento()