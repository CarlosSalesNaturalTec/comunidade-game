// =============================================================================
//  Comunidade Game — Sensor de temperatura do território (ESP32)
// =============================================================================
//
//  O que este programa faz, a cada INTERVALO_MINUTOS:
//    1. liga o Wi-Fi e acerta o relógio pela internet (NTP);
//    2. mede a temperatura três vezes e fica com o valor do meio (mediana);
//    3. guarda a medição com a hora em que ela aconteceu;
//    4. envia ao Backend API do Comunidade Game todas as medições guardadas,
//       da mais antiga para a mais nova;
//    5. desliga o Wi-Fi e dorme até a próxima medição.
//
//  Sem internet, as medições ficam guardadas (até 48) e seguem quando a rede
//  voltar: a plataforma vale a HORA DA MEDIÇÃO, não a hora do envio.
//
//  Você só precisa abrir o arquivo config.h e preencher o Wi-Fi.
//
//  Placa na Arduino IDE: "ESP32 Dev Module" (pacote esp32 da Espressif).
//  Bibliotecas (Gerenciador de Bibliotecas da Arduino IDE):
//    - DS18B20: "OneWire" (Paul Stoffregen) e "DallasTemperature" (Miles Burton)
//    - DHT22/DHT11: "DHT sensor library" (Adafruit) e "Adafruit Unified Sensor"
// =============================================================================

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <time.h>
#include "esp_sleep.h"

#include "config.h"

#if defined(SENSOR_DS18B20)
  #include <OneWire.h>
  #include <DallasTemperature.h>
  OneWire barramento(PINO_DO_SENSOR);
  DallasTemperature sonda(&barramento);
#elif defined(SENSOR_DHT22) || defined(SENSOR_DHT11)
  #include <DHT.h>
  #if defined(SENSOR_DHT22)
    DHT dht(PINO_DO_SENSOR, DHT22);
    #define ESPERA_ENTRE_LEITURAS_MS 2200
  #else
    DHT dht(PINO_DO_SENSOR, DHT11);
    #define ESPERA_ENTRE_LEITURAS_MS 1200
  #endif
#else
  #error "Escolha um sensor em config.h (SENSOR_DS18B20, SENSOR_DHT22 ou SENSOR_DHT11)."
#endif

// --- Fila de medições ainda não enviadas -------------------------------------
//  RTC_DATA_ATTR: a fila sobrevive ao sono profundo (some se faltar energia).
#define TAMANHO_DA_FILA 48

struct Medicao {
  time_t momento;  // segundos desde 1970, em UTC
  float valor;
};

RTC_DATA_ATTR Medicao fila[TAMANHO_DA_FILA];
RTC_DATA_ATTR int tamanhoDaFila = 0;
RTC_DATA_ATTR uint32_t ciclos = 0;

// Relógio considerado certo a partir de 2024-01-01.
static const time_t RELOGIO_MINIMO = 1704067200;

// --- LED de aviso ------------------------------------------------------------
void piscar(int vezes, int duracaoMs) {
  for (int i = 0; i < vezes; i++) {
    digitalWrite(PINO_DO_LED, HIGH);
    delay(duracaoMs);
    digitalWrite(PINO_DO_LED, LOW);
    delay(duracaoMs);
  }
}

// --- Wi-Fi e relógio -----------------------------------------------------------
bool conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NOME, WIFI_SENHA);
  Serial.printf("Conectando ao Wi-Fi \"%s\"", WIFI_NOME);
  unsigned long inicio = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - inicio < 20000) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Sem Wi-Fi. Confira nome e senha em config.h e se a rede é 2,4 GHz.");
    return false;
  }
  Serial.printf("Conectado. Sinal: %d dBm\n", WiFi.RSSI());
  return true;
}

void desligarWiFi() {
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
}

bool relogioCerto() {
  return time(nullptr) > RELOGIO_MINIMO;
}

void acertarRelogio() {
  configTzTime(FUSO_HORARIO, "a.st1.ntp.br", "b.st1.ntp.br", "pool.ntp.org");
  struct tm agora;
  if (getLocalTime(&agora, 10000)) {
    Serial.printf("Relógio acertado: %02d/%02d/%04d %02d:%02d\n", agora.tm_mday,
                  agora.tm_mon + 1, agora.tm_year + 1900, agora.tm_hour, agora.tm_min);
  } else {
    Serial.println("Não consegui acertar o relógio pela internet.");
  }
}

// --- Leitura do sensor ---------------------------------------------------------
float lerUmaVez() {
#if defined(SENSOR_DS18B20)
  sonda.requestTemperatures();
  float t = sonda.getTempCByIndex(0);
  // -127 = sonda desligada; 85 = valor de partida, ainda sem medir de verdade.
  if (t == DEVICE_DISCONNECTED_C || t == 85.0f) return NAN;
  return t;
#else
  delay(ESPERA_ENTRE_LEITURAS_MS);
  return dht.readTemperature();
#endif
}

float medirTemperatura() {
  float v[3];
  int validas = 0;
  for (int i = 0; i < 3; i++) {
    float t = lerUmaVez();
    if (!isnan(t)) v[validas++] = t;
  }
  if (validas == 0) return NAN;
  // Mediana simples: ordena e pega o do meio.
  for (int i = 0; i < validas; i++)
    for (int j = i + 1; j < validas; j++)
      if (v[j] < v[i]) { float x = v[i]; v[i] = v[j]; v[j] = x; }
  return v[validas / 2];
}

// --- Fila ----------------------------------------------------------------------
void guardarNaFila(time_t momento, float valor) {
  if (tamanhoDaFila == TAMANHO_DA_FILA) {
    // Fila cheia: descarta a mais antiga para caber a nova.
    for (int i = 1; i < TAMANHO_DA_FILA; i++) fila[i - 1] = fila[i];
    tamanhoDaFila--;
    Serial.println("Fila cheia: a medição mais antiga foi descartada.");
  }
  fila[tamanhoDaFila++] = {momento, valor};
}

void tirarDaFila() {
  for (int i = 1; i < tamanhoDaFila; i++) fila[i - 1] = fila[i];
  tamanhoDaFila--;
}

// --- Envio ao Backend API ------------------------------------------------------
String codificarParaFormulario(const char* texto) {
  String saida;
  const char* hex = "0123456789ABCDEF";
  for (const unsigned char* p = (const unsigned char*)texto; *p; p++) {
    if (isalnum(*p) || *p == '-' || *p == '_' || *p == '.' || *p == '~') {
      saida += (char)*p;
    } else {
      saida += '%';
      saida += hex[*p >> 4];
      saida += hex[*p & 0x0F];
    }
  }
  return saida;
}

String momentoEmTexto(time_t momento) {
  // Envia em UTC ("Z"): a plataforma guarda data e hora com fuso.
  struct tm utc;
  gmtime_r(&momento, &utc);
  char texto[25];
  strftime(texto, sizeof(texto), "%Y-%m-%dT%H:%M:%SZ", &utc);
  return String(texto);
}

// Resultado de um envio: o que fazer com a medição.
enum Resultado { ENVIADA, RECUSADA_DESCARTAR, BARRADA_PARAR, FALHA_TENTAR_DEPOIS };

Resultado enviar(const Medicao& m) {
  WiFiClientSecure cliente;
  if (TESTE_SEM_CERTIFICADO) {
    cliente.setInsecure();
  } else {
    cliente.setCACert(CA_RAIZ);
  }

  HTTPClient http;
  http.setTimeout(15000);
  String url = String(URL_DA_API) + "/v1/registros-de-coleta";
  if (!http.begin(cliente, url)) return FALHA_TENTAR_DEPOIS;

  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.addHeader("X-Chave-Aplicacao", CHAVE_DA_APLICACAO);
  http.addHeader("X-Credencial-Dispositivo", CREDENCIAL_DO_DISPOSITIVO);

  String corpo = String("serie_de_coleta_id=") + codificarParaFormulario(SERIE_DE_COLETA_ID) +
                 "&momento_do_fato=" + codificarParaFormulario(momentoEmTexto(m.momento).c_str()) +
                 "&origem=sensor" +
                 "&valor=" + String(m.valor, 1) +
                 "&unidade=" + codificarParaFormulario(UNIDADE);

  int codigo = http.POST(corpo);
  String resposta = codigo > 0 ? http.getString() : String();
  http.end();

  Serial.printf("  %s  %.1f %s -> HTTP %d\n", momentoEmTexto(m.momento).c_str(), m.valor,
                UNIDADE, codigo);

  if (codigo == 201) {
    if (resposta.indexOf("\"a_conferir\":true") >= 0)
      Serial.println("  (valor fora da faixa esperada: entrou como \"a conferir\")");
    return ENVIADA;
  }
  // 400/404/422: a plataforma nunca vai aceitar esta medição (ex.: fora da
  // vigência do desafio). Mostra o motivo e descarta.
  if (codigo == 400 || codigo == 404 || codigo == 422) {
    Serial.println("  Recusada: " + resposta);
    return RECUSADA_DESCARTAR;
  }
  // 401/403: chave de aplicação ou credencial do dispositivo inválida,
  // revogada, ou a série foi encerrada. Avise o Mestre.
  if (codigo == 401 || codigo == 403) {
    Serial.println("  Barrada: confira a chave e a credencial com o Mestre. " + resposta);
    return BARRADA_PARAR;
  }
  // Sem resposta, 429 ou 5xx: tenta de novo no próximo ciclo.
  return FALHA_TENTAR_DEPOIS;
}

void enviarFila() {
  Serial.printf("Enviando %d medição(ões)...\n", tamanhoDaFila);
  while (tamanhoDaFila > 0) {
    Resultado r = enviar(fila[0]);
    if (r == ENVIADA) {
      tirarDaFila();
      piscar(1, 80);
    } else if (r == RECUSADA_DESCARTAR) {
      tirarDaFila();
    } else if (r == BARRADA_PARAR) {
      piscar(5, 400);
      return;
    } else {
      piscar(3, 120);
      return;
    }
  }
}

// --- Um ciclo completo -----------------------------------------------------------
void ciclo() {
  ciclos++;
  digitalWrite(PINO_DO_LED, HIGH);
  Serial.printf("\n=== Ciclo %lu ===\n", (unsigned long)ciclos);

  bool online = conectarWiFi();
  if (online) acertarRelogio();

  float t = medirTemperatura();
  if (isnan(t)) {
    Serial.println("Sensor sem leitura. Confira os fios e o resistor de 4,7 kΩ.");
    piscar(2, 400);
  } else if (!relogioCerto()) {
    // Sem hora certa não há registro: a plataforma exige a hora da medição.
    Serial.printf("Medi %.1f %s, mas o relógio ainda não foi acertado. Descartada.\n", t,
                  UNIDADE);
  } else {
    Serial.printf("Temperatura: %.1f %s\n", t, UNIDADE);
    guardarNaFila(time(nullptr), t);
  }

  if (online && tamanhoDaFila > 0) enviarFila();
  Serial.printf("Ficaram %d medição(ões) guardada(s).\n", tamanhoDaFila);

  desligarWiFi();
  digitalWrite(PINO_DO_LED, LOW);
}

// --- Arduino -----------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(200);
  pinMode(PINO_DO_LED, OUTPUT);
  setenv("TZ", FUSO_HORARIO, 1);
  tzset();

#if defined(SENSOR_DS18B20)
  sonda.begin();
  sonda.setResolution(12);
#else
  dht.begin();
#endif

  ciclo();

  if (USAR_SONO_PROFUNDO) {
    Serial.printf("Dormindo %d minuto(s).\n", INTERVALO_MINUTOS);
    Serial.flush();
    esp_sleep_enable_timer_wakeup((uint64_t)INTERVALO_MINUTOS * 60ULL * 1000000ULL);
    esp_deep_sleep_start();  // acorda de novo no setup()
  }
}

void loop() {
  // Só chega aqui com USAR_SONO_PROFUNDO = false.
  static unsigned long ultimo = millis();
  if (millis() - ultimo >= (unsigned long)INTERVALO_MINUTOS * 60UL * 1000UL) {
    ultimo = millis();
    ciclo();
  }
  delay(1000);
}
