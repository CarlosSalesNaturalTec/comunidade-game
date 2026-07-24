<div align="center">
<img src="/static/images/logo.png" alt="Logo">
</div>

<hr>

[English Version](/README.md)

![Portuguese](https://img.shields.io/badge/Language-English-blue)
<hr>

## 🤓 Aprenda a programar construindo seu próprio robô.

Robô Educa  é uma plataforma inovadora que ensina programação para crianças de 6 a 14 anos, promovendo a inclusão e a sustentabilidade 🤝♻️. A jornada começa com uma história inspiradora de dois irmãos, Suzy e Otávio, que desejam construir um robô 🤖 e contam com a ajuda de seu professor Carlos Sales 👨‍🏫 que os incentiva a montar seu próprio robô humanoide utilizando materiais reciclados, programação e nuvem ♻️💻☁️.

É neste contexto que surge o Web Aplicativo Robô Educa que acessível a partir de qualquer smartphone 📱 se torna o "cérebro" do robô 🧠 interagindo com a criança através de  mensagens de áudio 🗣️ tornando-o acessível inclusive para pessoas com deficiência visual. A montagem do robô e a interação com o aplicativo estimulam a coordenação motora 🖐️ e a criatividade ✨ ensinando a criança conceitos tecnológicos de forma lúdica e inclusiva.

E toda a mágica realizado pelo aplicativo só é possível por conta do uso da **Google GEMINI API** 🤖 que permite ao Robô Educa entender e responder às perguntas da criança, explicar conceitos complexos 🤯 e realizar quizzes gamificados 🎉. Essa tecnologia disponível na nuvem da Google transforma o aprendizado em uma conversa natural e divertida 😄 abrindo novas perspectivas para o futuro destas crianças 🚀.

## 🤖 Como testar o aplicativo:
* Acesse : https://robo-educa-gemini-server-xd3gd6y2aa-uw.a.run.app/
* Clique em Iniciar;
* Autorize o uso do Microfone;
* Clique em: ENTRAR COMO VISITANTE;
* Ouça as perguntas e responda corretamente para acumular pontos.

## 💪 Histórico de Impacto Social

Desde o ano de 2018 este trabalho, que acontece de forma voluntária, já impactou centenas de crianças em diversas comunidades carentes na cidade de **Salvador, Bahia - Brasil**.

O idealizador deste projeto, [Carlos Sales](https://drive.google.com/file/d/1KPPJQhNn_YsWYK6qllP6muns6WlSRyM1/view?usp=sharing), é um homem negro de origem periférica graduado em Ciência de Dados e Desenvolvedor de Sistemas. O mesmo conta um pouco da sua história no documentário [C0d3rs Championship](https://www.primevideo.com/detail/0GS98CG03BVM7C224YK7KIWXOJ) disponível no Amazon Prime Video.

Mas foi somente no ano de 2024 com o advento das **IA Generativas** e da **Google GEMINI API**, que o robô passou a ter um **cérebro** capaz de responder de forma inteligente e rápida, tornando a interação muito mais flúida e encantadora 😄!

<div style="display: flex;">
<img src="/static/images/image1.jpg" alt="Imagem 1" style="width: 22%; margin-right: 8px;">
<img src="/static/images/image2.jpg" alt="Imagem 2" style="width: 22%; margin-right: 8px;">
<img src="/static/images/image3.jpg" alt="Imagem 3" style="width: 22%; margin-right: 8px;">
<img src="/static/images/image4a.jpg" alt="Imagem 4" style="width: 22%;">
</div>

#### 📸 Visite nossa [galeria de fotos](https://photos.app.goo.gl/yJiewdTTsNFtmF846) para conhecer mais sobre nossas oficinas de inclusão digital.

#### 📢 Assista o [depoimento](https://youtu.be/rjb9G7iBl8Q) de diretores, professores e alunos que já utilizaram nossa plataforma.

## Como as coisas funcionam

### 👤 CORPO

A plataforma **Robô Educa** oferece uma experiência prática e criativa para os alunos, orientando-os na montagem física de um robô humanoide. Este robô pode ser feito com materiais recicláveis como garrafas PET ♻️ ou kits em madeira MDF. Após a montagem física, os alunos dão vida ao robô usando o "cérebro" dele 🧠, que é o aplicativo contido neste repositório.

<div style="display: flex;">
<img src="/static/images/robopet1.jpg" alt="Robo Educa Versão Garrafa PET" style="width: 22%; margin-right: 8px;">
<img src="/static/images/robopet2.jpg" alt="Robô Educa em MDF versão 1" style="width: 22%; margin-right: 8px;">
<img src="/static/images/robopet3.jpg" alt="Robô Educa em MDF versão 2" style="width: 22%; margin-right: 8px;">
<img src="/static/images/robopet4.jpg" alt="Robô Educa em MDF manuseado por criança" style="width: 22%;">
</div>

### 🧠 CÉREBRO

O aplicativo, cérebro do robô, permite que o mesmo desempenhe funções cognitivas como ouvir, pensar e falar. 

#### Tecnologias utilizadas na construção do aplicativo

<div align="center">
<img src="/static/images/gemini.png" alt="Logo Build with Gemini">
</div>

- ![Pyton](https://img.shields.io/badge/python-v3-green)
- ![HTML](https://img.shields.io/badge/HTML-5-orange)
- ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
- ![Firestore](https://img.shields.io/badge/Firebase-Firestore-orange?style=for-the-badge&logo=firebase)
- ![Google Cloud](https://img.shields.io/badge/Google_Cloud-gray?style=for-the-badge&logo=google-cloud)

<hr>

### Arquitetura

A aplicação é desenvolvida utilizando ferramentas open-source e hospedada na **Google Cloud**, aproveitando sua infraestrutura robusta. O backend é desenvolvido em Python usando o framework Flask, seguindo o padrão de design **Service/Repository**:

- **Camada de Serviço**: Lida com a lógica de negócio.
- **Camada de Repositório**: Gerencia a integração com o banco de dados.

Para armazenamento de dados, a plataforma utiliza um banco de dados NoSQL, o **Firebase/Firestore**, que oferece escalabilidade e flexibilidade para armazenar conversas e dados de usuários.

### Arquivos Principais e Funcionalidades

![Pyton](https://img.shields.io/badge/python-v3-green)

### Backend - `routes.py`
O arquivo `routes.py` gerencia todas as rotas disponíveis na aplicação. É aqui que diferentes endpoints são definidos para lidar com as interações dos usuários e o processamento de dados.

```python
# Dependências
from main import app
from flask import render_template, request, session, redirect, url_for, make_response, jsonify
# Serviços
import service.loginService as loginService
import service.talkService as talkService

# Página inicial/Index
@app.route('/')
def home():
    return render_template('index.html')

# Troca de mensagens entre usuário e bot
@app.route('/talk', methods=['POST']) 
def talk():   
    # Verifica se usuário está logado       
    if not session.get('userId'): return make_response(jsonify({"error": "Não autorizado"}), 401)

    # obtem dados da requisição - mensagem do usuário
    data = request.get_json()
    userMessage = data.get('message')    

    # Envia mensagem para Bot e aguarda respectiva resposta
    botResponse = talkService.talk(userMessage)
    
    # retorna ao Front com resposta do Bot
    return botResponse    
```

### Frontend - HTML, CSS e JavaScript

![HTML](https://img.shields.io/badge/HTML-5-orange)

O frontend é implementado utilizando HTML, CSS e JavaScript, focando na simplicidade e facilidade de uso. Ele começa solicitando o acesso ao microfone, que é gerenciado pelo `/static/js/mediadevices.js`.

#### Acesso ao Microfone:

![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)

Quando o aplicativo é iniciado, ele verifica as permissões para uso do microfone. Se for a primeira vez que o usuário acessa o app, ele será solicitado a conceder a permissão. Este processo é gerenciado pelo arquivo `/static/js/mediadevices.js`.

```javascript
async function devices_micPrompt() {
    let permission;
    await navigator.mediaDevices
        .getUserMedia({
            audio: true
        })
        .then(function (stream) {
            permission = "granted"        
        })
        .catch(function (error) {
            if (error.message == "Requested device not found") {
                permission = "notFound";
            } else if (error.message == "Permission denied") {
                permission = "denied";
            } else {
                console.log(error.message)
                permission = 'error';
            }
        });
    return permission;
}
```

#### Autenticação do Usuário:
O processo de login é gerenciado pelo arquivo `/static/js/login.js`, que envia uma requisição POST para o backend para validar o usuário. Se o usuário não tiver credenciais válidas, ele pode fazer login como convidado.

```javascript
async function login(usertype) {    

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;    

    displayStartLogin();
    
    await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password, usertype: usertype })
    })
    .then(response => response.json())
    .then(data => {

        displayStopLogin();
        
        switch (data.status) {
            case 'success':
                goToPage("interaction");
                break;
            case 'errorUser':
                alert("Usuário inexistente");
                document.getElementById("username").focus();
                break;
            case 'errorPwd':
                alert("Senha incorreta");
                document.getElementById("password").focus();
                break;
            case 'errorGuest':
                alert("Não foi possível criar usuário temporário. Tente novamente!");                
                break;                
            default:
                break;
        }        
    });
    
}
```

#### Interação:
Após o login bem-sucedido, a interação começa no frontend com o arquivo `templates/interaction.html`. A interface visual, gerenciada pelo arquivo `statis/js/display.js`, é simples, com elementos que simbolizam escuta, pensamento e fala.

**Escuta Contínua e Processamento de Fala**:
O robô começa com uma saudação e convida o usuário a participar de um quiz sobre programação. Após falar, o app ativa o microfone em modo contínuo, escutando o que o usuário fala. Essas tarefas são realizadas pelo arquivo `/static/js/talk.js`, que utiliza as APIs `Media Devices`, `SpeechRecognition()` e `SpeechSynthesisUtterance()`.

#### 🦻 OUVIR

![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)

```javascript
recognition = new SpeechRecognition();
recognition.lang = "pt-BR";
recognition.continuous = true;      // Reconhecimento contínuo em loop
recognition.interimResults = false; // resultados parciais

// Este evento é acionado quando o reconhecimento de voz captura um resultado
recognition.onresult = event => {    
    const transcript = event.results[event.resultIndex][0].transcript;    
    talk(transcript);           // Envia transcrição do audio falado pelo usuário para o backend processar junto à Inteligência Artificial e dar uma respectiva resposta
};

// Verifica se usuário não estiver falando (reproduzindo audio). Após 1 minuto de inatividade, interrrompe reconhecimento e exibe botão de pausa
recognition.onend = () => {
    if (speakStatus == false) {     
        timestampAtual = Date.now();
        var diferenca = timestampAtual - timestampParam;
        var minutosPassados = diferenca / (1000 * 60);
        if (minutosPassados < 1) {
            recognition.start(); // Inicia o reconhecimento de voz
        } else {
            hideAllExceptClose();
            showElement("divPauseStart");
        }
    }        
};
```

#### 🗣️ FALAR

![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)

```javascript
// Sintese de Fala - faz o dispositivo reproduzir uma mensagem através de seus autofalantes/fones
function speak(message) {
    message = removerEmojis(message);
    const utterThis = new SpeechSynthesisUtterance(message);
    utterThis.pitch = 2;
    utterThis.rate = 4;

    utterThis.onstart = function () {
        hideAllExceptClose();                   // Oculta elementos que estiverem visiveis na tela
        showElement("divSpinnerWaves");                
    };

    utterThis.onend = function () {        
        speakStatus=false;
        hideAllExceptClose();                   // Oculta elementos que estiverem visiveis na tela
        showElement("divSpinnerRipple");        // Exibe Spinner simulando ondulaçao de escuta 
        recognition.start();                    // Inicia o reconhecimento de voz 
        timestampParam = Date.now();       
    };

    recognition.stop();                         // Ao iniciar a fala (reprodução do audio) Interrompe o reconhecimento de voz
    speakStatus=true;                           // Speaking     on=true  off=false
    synth.speak(utterThis);                     // inicia a reprodução da mensagem    
}

// Remove emojis da mensagem, para que a mesma possa ser reproduzida via sintese de fala
function removerEmojis(texto) {
    return texto
        .replace(/\p{Emoji}/gu, '') // Remove emojis
        .replace(/\s+/g, ' ') // Remove espaços em branco extras
        .trim(); // Remove espaços em branco no início e no fim
}
```

### 🧠 Processamento Cognitivo com a API Google Gemini

![Google Cloud](https://img.shields.io/badge/Google_Cloud-gray?style=for-the-badge&logo=google-cloud)

#### Rapidez nas respostas utilizando o modelo: **gemini-1.5-flash** 

Quando uma frase completa é detectada, ela é enviada para o backend para processamento cognitivo. Esta tarefa é realizada pela **API do GEMINI**, utilizando o modelo `gemini-1.5-flash` que produz respostas rápidas e precisas, garantindo conversas fluidas que tornam o robô mais **envolvente e realista**.

#### Engenharia de Prompt

Utilizamos a técnica **Zero-Shot Prompting** aliada a um recurso do SDK do GEMINI, as **System instructions**, que fornecem um quadro de referência para o modelo, ajudando-o a compreender a tarefa e a responder de forma adequada sem precisar de exemplos específicos.

```python
import google.generativeai as genai

genai.configure(api_key=my_api_key)

system_instruction = os.environ.get("SYSTEM_INSTRUCTIONS")    # Gemini - Instruções do Sistema / Informa as caracteristicas do Assistente.

model = genai.GenerativeModel(model_name=ai_model,
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings)

# Interação com a Google Gemini API
def talk(userMessage):
    # Obtem ID do usuário logado
    user_id = session["userId"]

    # Obtem histórico de mensagens do usuário
    message_history = messageHistory.getById(user_id)
    message_history_gemini_format = format_messages_for_gemini(message_history)   
    
    # Salva mensagem do usuário em banco de dados
    role = "user"                                       # role=user => mensagem enviada pelo usuário
    messageHistory.store(user_id, role, userMessage)    

    # Inicia interação com Gemini AI
    try:
        convo = model.start_chat(history = message_history_gemini_format) # Inicia chat, contextualizando a IA com o histórico da conversação
        convo.send_message(userMessage)                     # envia nova mensagem para ser processada pela IA
        bot_response = convo.last.text                      # Obtem resposta da IA
    except:
        bot_response = "error"

    # Salva resposta do Bot em banco de dados
    if bot_response != "error":
        role = "model"                                      # role=model => mensagem enviada pela IA
        messageHistory.store(user_id, role, bot_response)    
    else:
        bot_response = "Desculpe, não foi possível obter resposta da Inteligência Artificial."

    response = {"status": "success", "message": bot_response}
    return response
```

### Configurando a criatividade das respostas

O parâmetro `generation_config` é utilizado para controlar o comportamento do modelo de linguagem durante a geração de texto. Ele contém várias configurações importantes que influenciam a criatividade, o foco e o tamanho das respostas do modelo. 

Em especial chamamos a atenção para a configuração de **TEMPERATURE'** que controla o grau de aleatoriedade nas respostas. Valores mais altos (próximos a 2) levam a resultados mais criativos e diversificados, mas podem ser menos previsíveis e eventualente podem conter erros/alucinações. Valores mais baixos (próximos a 0) geram respostas mais focadas e conservadoras, porém, tendendo a repetir padrões comuns. 

A configuração `max_output_tokens` define o número máximo de tokens (palavras ou subpalavras) que o modelo pode gerar na resposta. Isso evita respostas excessivamente longas e ajuda a controlar o tempo de processamento.

```python
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192  
}
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel(model_name=ai_model,
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings)
```

### 🛡️ Conteúdo para crianças - Segurança no comportamento do modelo 

A **Google Gemini API** oferece uma funcionalidade chamada `safety_settings` que permite controlar o comportamento do modelo de linguagem em relação à segurança, especialmente em conversas com crianças. Ao instanciar o modelo é possível definir os níveis desejados de proteção contra conteúdo impróprio ou perigoso.

```python
safety_settings = [  
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  }
]
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel(model_name=ai_model,
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings)
```

Sendo:

 **category**: A categoria específica de conteúdo prejudicial que você deseja bloquear. As categorias disponíveis são:

* HARM_CATEGORY_HARASSMENT: Bloqueia conteúdo que pode ser considerado bullying, assédio ou perseguição.
* HARM_CATEGORY_HATE_SPEECH: Bloqueia conteúdo que promove o ódio, a violência ou a discriminação contra grupos específicos.
* HARM_CATEGORY_SEXUALLY_EXPLICIT: Bloqueia conteúdo sexualmente explícito ou sugestivo.
* HARM_CATEGORY_DANGEROUS_CONTENT: Bloqueia conteúdo que pode ser considerado perigoso, como instruções para atividades perigosas ou informações sobre como fabricar armas.

E:

**threshold**: O parâmetro que define o nível de rigor com que o modelo deve bloquear conteúdo dentro de uma determinada categoria. O valor selecionado foi:

**BLOCK_LOW_AND_ABOVE**: Bloqueia qualquer conteúdo dentro da categoria que seja considerado "baixo", "médio" ou "alto" em termos de risco. Este é o nível de segurança mais alto e é adequado para ambientes onde a proteção de crianças é priorizada.

### Armazenamento de Dados

![Firestore](https://img.shields.io/badge/Firebase-Firestore-orange?style=for-the-badge&logo=firebase)

A plataforma armazena a conversa de cada usuário em um banco de dados do **Firestore** utilizando coleções NoSQL. Isto gera vários benefícios:

* Escalabilidade automática: O Firestore é um banco de dados NoSQL que escala automaticamente, ajustando-se à demanda de forma transparente, garantindo que o aplicativo possa lidar com um grande volume de conversas sem problemas de desempenho.
* Baixa latência: O Firestore é projetado para operações de leitura e gravação rápidas, tornando as respostas do chatbot instantâneas e fluidas.
* Segurança e controle de acesso: O Firestore oferece controle de acesso granular, permitindo definir regras para quem pode acessar e modificar as conversas, garantindo a privacidade e segurança dos dados.
* Modelo de preços baseado em uso: Você paga apenas pelos recursos que usa, o que pode ser mais econômico em comparação com bancos de dados relacionais tradicionais, especialmente para aplicações de chatbot com alto volume de conversas.
* Permite a moderação das conversas, para controle de qualidade e segurança da comunicação;
* Permite a personalização do conteúdo. 

```python
import time
import repository.db_resource as dbr

# Instância de conexão com banco de dados NoSQL Google Firestore
db = dbr.firestore_resource()       

# Obtem histórico de mensagens a partir do ID do usuário
def getById(user_id):
    collection = f"message_history_{user_id}"
    messages_ref = db.collection(collection).order_by("timestamp")
    messages = messages_ref.stream()

    return messages

# Salva mensagem para recuperação de histórico de conversa na contextualização da resposta
def store(user_id, role, message):
    collection = f"message_history_{user_id}"
    try:
        doc_ref = db.collection(collection).document()
        doc_ref.set({
            "timestamp": int(time.time()),
            "role": role,
            "parts": [message]
        })    
    except Exception as e:
        print(f"Erro ao salvar mensagem no banco de dados. Detalhes: {e}")
        return False
```

### 🎯 Personalização do conteúdo

E com relação a personalização de conteúdo, O **Google GEMINI** é capaz de lidar com até **2 milhões de Tokens**. O que representa um volume de dados considerável, capaz de armazenar uma quantidade significativa de informações e interações para a personalização de conteúdo educacional.

Algumas aplicações práticas para uso desta capacidade:

1. Históricos de Aprendizagem Detalhados: 

***Mapeamento do Progresso***: Armazenar o histórico completo de interações de um aluno, como respostas a exercícios, testes, debates, feedback, tempo dedicado a cada assunto, etc., permite mapear o progresso de forma individualizada e granular.

***Identificação de Padrões***: Analisar esses dados permite identificar padrões de comportamento, áreas de dificuldade, pontos fortes e estilos de aprendizagem de cada aluno.

2. Criação de Rotas de Aprendizagem Personalizadas:

***Recomendador Inteligente***: Com base no histórico, o sistema pode recomendar conteúdo, atividades, exercícios e recursos específicos para cada aluno, adaptando o ritmo e o nível de dificuldade.

***Conteúdo sob Demanda:*** O modelo pode gerar material de apoio, explicações adicionais, resumos ou exemplos sobre tópicos específicos onde o aluno demonstra dificuldades.

3. Feedback Personalizado e Interativo:

***Análise de Respostas:*** O modelo pode analisar respostas, identificando erros, lacunas de conhecimento e áreas que precisam de reforço.

***Feedback Adaptativo:*** O feedback pode ser personalizado com explicações claras, exemplos e dicas específicas para cada aluno, aumentando o aprendizado e a retenção.

### ✅ Conclusão

O Robô Educa combina criatividade física com inteligência artificial de ponta para criar uma experiência interativa e educacional para crianças. A arquitetura modular da plataforma e o uso de tecnologias web modernas a tornam escalável, segura e adaptável a diversos ambientes de aprendizado.

## 💻 Como executar este aplicativo em seu PC Windows

1. Clone o repositório:
```
$ git clone https://github.com/Robo-Educa/robo-educa-gemini-server.git 
```
2. Instale as dependências:
```
$ cd robo-educa-gemini-server
$ pip install -r requirements.txt
```
3. Crie um arquivo .ENV a partir do .ENV.EXAMPLE e preencha os valores das variáveis de ambiente conforme o seu projeto.

4. Execute o projeto:
```
$ python main.py
```
5. Teste no Navegador:
```
http://localhost:5000
```
## ☁️ Como realizar deploy no ambiente de nuvem da Google (Cloud Run)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-gray?style=for-the-badge&logo=google-cloud)
* No console da Google Cloud Platform, crie um Projeto 
* Certifique-se de ter instalado em seu PC Windows a CLI gcloud (Google Cloud SDK Shell)
* Em um terminal do Google Cloud SDK Shell, vá para a pasta em que se encontra o seu projeto e inicialize sua conexão informando o seu email, projeto e região default para hospedagem do seu App:
```
$ cd\[path do projeto]
$ gcloud init
```
* Faça o deploy do seu App:
```
$ gcloud run deploy --source .
```
* No console da Google Cloud Platform, selecione o seu projeto.
* No menu de navegação selecione: FireBase-Firestore 
* Crie um Banco de Dados do tipo Nativo
* Baixe um arquivo JSON contendo credenciais de acesso ao seu banco:
    * IAM e Administrador / Contas de Serviço / Clicar na conta de Serviço: **Default compute service account**
    * Chaves / Adicionar chave / Criar nova Chave / JSON / Criar
    * O arquivo JSON será baixado automaticamente
* No menu de navegação selecione: Google Cloud Storage
* Crie um Bucket privado. Salve neste Bucket o arquivo JSON contendo credencial de acesso ao banco de dados
* No menu de navegação selecione: Cloud Run 
* Clique no Aplicativo 
* Clique em: "Editar e implantar uma nova versão"
    * Clique em Volumes / Adicionar um Volume referente ao Bucket contendo a credencial do banco de dados
        * Tipo: Bucket do Cloud Storage
        * Acessar a Guia Containers / Montagem de Volumes / Montar Volume
        * Selecionar o nome do volume criado 
        * Caminho da Montagem : especificar um nome que servirá como path. Ex: /config
        * Concluir / Implantar
* Clique novamente em: Editar e implantar uma nova versão    
    * Variáveis e Secrets / Adicione as mesmas variáveis contidas n arquivo .ENV.example
        * Atenção para variável PATH_CREDENTIAL_FIRESTORE que deverá conter o path do volume recém criado. Ex: /config/credencial.json
        * Atenção para variável API_KEY que deverá conter uma chave válida que pode ser obtida em : https://aistudio.google.com
* Atenção: Cuidado com o arquivo JSON contendo a credencial de acesso ao banco de dados e também com sua API_KEY Gemini. Nunca os exponha publicamente, utilize secrets ou outros recusos de seguranças recomendados pela plataforma Google Cloud.

## 📄 Licença

Este projeto está licenciado sob a [Apache 2.0 License](LICENSE). Observe também os Termos de Serviço.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou colaborar de qualquer outra forma.

💪 E você? Gostou? Então faça sua parte e colabore com esta iniciativa para que possamos ampliar ainda mais o nosso impacto.


* Contatos/WhatsApp: +55 (71) 9.9341-6896 
* E-mail: roboeduca.net@gmail.com

<div style="display: flex;">
<img src="/static/images/ods1.jpg" alt="Ods 4" style="width: 30%; margin-right: 5px;">
<img src="/static/images/ods2.jpg" alt="ODS ONU" style="width: 30%; margin-right: 5px;">
<img src="/static/images/ods3.jpg" alt="Ods 10" style="width: 30%;">
</div>