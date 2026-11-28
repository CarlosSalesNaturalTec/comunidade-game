// =============================================================================
//  Comunidade Game — Sensor de temperatura do território
//  config.h — o ÚNICO arquivo que você precisa abrir.
// =============================================================================
//
//  PARTE 1 — você (Guerreiro ou Guerreira) preenche: a rede Wi-Fi do local.
//  PARTE 2 — já vem preenchida pela plataforma (ou pelo Mestre). NÃO mexa.
//  PARTE 3 — ajustes da montagem. Só mude se o Mestre pedir.
//
// =============================================================================
#pragma once

// -----------------------------------------------------------------------------
//  PARTE 1 — A SUA REDE WI-FI
// -----------------------------------------------------------------------------
//  Escreva entre as aspas o nome da rede e a senha, exatamente como aparecem
//  no celular (maiúsculas e minúsculas contam). O ESP32 só conecta em rede de
//  2,4 GHz — rede "5G" não funciona.
#define WIFI_NOME   "nome-da-rede-aqui"
#define WIFI_SENHA  "senha-da-rede-aqui"

// -----------------------------------------------------------------------------
//  PARTE 2 — DADOS DA PLATAFORMA (não mexa)
// -----------------------------------------------------------------------------
//  Endereço do Backend API, sem barra no fim.
#define URL_DA_API                "https://api.exemplo.comunidadegame"

//  Chave de aplicação (cabeçalho X-Chave-Aplicacao).
#define CHAVE_DA_APLICACAO        "coloque-a-chave-de-aplicacao"

//  Credencial do dispositivo, no formato  identificador.segredo
//  (cabeçalho X-Credencial-Dispositivo). O segredo aparece UMA vez só,
//  quando o Mestre emite a credencial — guarde este arquivo com cuidado e
//  nunca publique em rede social, grupo ou repositório público.
#define CREDENCIAL_DO_DISPOSITIVO "identificador.segredo"

//  A série de coleta que este sensor alimenta (UUID).
#define SERIE_DE_COLETA_ID        "00000000-0000-0000-0000-000000000000"

//  Unidade exatamente como o tipo de coleta declara na plataforma.
#define UNIDADE                   "°C"

//  Certificado raiz da cadeia HTTPS do Backend API (formato PEM).
//  Vem preenchido pela plataforma. Para a hospedagem atual (Cloud Run), é o
//  "GTS Root R1" da Google Trust Services (pki.goog/repository).
static const char CA_RAIZ[] = R"PEM(
-----BEGIN CERTIFICATE-----
COLE-AQUI-O-CERTIFICADO-RAIZ
-----END CERTIFICATE-----
)PEM";

// -----------------------------------------------------------------------------
//  PARTE 3 — AJUSTES DA MONTAGEM
// -----------------------------------------------------------------------------
//  Qual sensor está ligado? Deixe UMA linha sem "//" na frente.
#define SENSOR_DS18B20     // sonda à prova d'água, fio de 1 m (recomendado)
// #define SENSOR_DHT22    // módulo branco, temperatura + umidade
// #define SENSOR_DHT11    // módulo azul, mais impreciso (±2 °C)

//  Pino de dados do sensor (GPIO). 4 é o "D4" da maioria das placas.
#define PINO_DO_SENSOR     4

//  LED de aviso. Na maioria das NodeMCU-32S / DevKit é o GPIO 2 (azul).
#define PINO_DO_LED        2

//  De quantos em quantos minutos medir. Combine com a cadência do desafio:
//  a plataforma só pontua a quantidade de registros por período que o
//  desafio declara — medir mais vezes não rende mais pontos.
#define INTERVALO_MINUTOS  30

//  true  = dorme entre medições (gasta pouco e esquenta menos a caixa).
//  false = fica ligado o tempo todo. Use false com power bank que desliga
//          sozinho quando o consumo cai (ver guia de montagem, §5).
#define USAR_SONO_PROFUNDO true

//  Fuso horário do relógio (Brasil, horário de Brasília, sem horário de verão).
#define FUSO_HORARIO       "<-03>3"

//  SÓ PARA TESTE DE BANCADA: true desliga a conferência do certificado HTTPS.
//  Nunca deixe true no sensor instalado.
#define TESTE_SEM_CERTIFICADO false
