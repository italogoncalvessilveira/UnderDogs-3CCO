*** Settings ***
Library            SeleniumLibrary
Library            DatabaseLibrary
Library            DateTime

*** Variables ***
                                                                                                                                                                         
${URL}            https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoicHQifQ%3D%3D%22%7D
${BROWSER}        Chrome
${TEXTO_EXTRAIDO}       

${DB_NAME}        Grupo3
${DB_USER}        admin
${DB_PASSWORD}    urubu100
${DB_HOST}        rds-underdogs.cfzmhji6igm5.us-east-1.rds.amazonaws.com
${DB_PORT}        3306


*** Keywords ***
Realiza Login
    [Arguments]    ${email}        ${senha}
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Sleep    5s    
    Input Text                     xpath=//input[@autocomplete='username']                                   text=${email}
    Sleep    5s    
    Click Element    //span[text()='Avançar'] 
    Sleep    5s    
    Input Text                     xpath=//input[@name='password']                                           text=${senha}
    Sleep    5s    
    Click Element    //span[text()='Entrar'] 
    Sleep    10s    
    Click Element    (//div[@class='css-1dbjc4n'])[3]
    Sleep    5s    



Busca Tema do Tweet
    [Arguments]    ${tema}
    Input Text                     xpath=//input[@placeholder='Search']                                           text=${tema}
    Sleep    5s    
    Click Element    //span[contains(text(),'Search for')]
    Sleep    5s    



Extrair Texto Com JavaScript
    [Arguments]    ${xpathExpression}
    ${textoExtraido}    Execute JavaScript
    ...        var elementos = document.evaluate('${xpathExpression}', document, null, XPathResult.ANY_TYPE, null);
    ...        var textoCompleto = '';
    ...        var elemento;
    ...        while ((elemento = elementos.iterateNext())) {
    ...            textoCompleto += elemento.textContent;
    ...        }
    ...        return textoCompleto.trim();
    [RETURN]        ${textoExtraido}




    
*** Test Cases ***
Pesquisa no Twitter por tema e Salva no Banco de Dados
    Realiza Login        ItaloRo46935377        Renato2002
    Busca Tema do Tweet        Qualidade do Sono
    ${VAR_FRASETWEET}        Extrair Texto Com JavaScript        (//article/div/div/div[2]/div[2]/div[2])[2]      
    Log    O texto extraído é: ${VAR_FRASETWEET} 
    Sleep    5s 

#   Insere no Banco de Dados Resultado da Pesquisa
    ${DATA_ATUAL}    Get Current Date    result_format=%Y-%m-%d %H:%M:%S 
    Connect To Database        pymysql        ${DB_NAME}    ${DB_USER}    ${DB_PASSWORD}    ${DB_HOST}    ${DB_PORT}
    Execute SQL String        INSERT INTO analise_twitter (fraseTweet, sentimentoTweet, origem, localizacao, horario_leitura) VALUES ('${VAR_FRASETWEET}', 'oi', 'Italo', 'Localhost', '${DATA_ATUAL}')
    Disconnect From Database

