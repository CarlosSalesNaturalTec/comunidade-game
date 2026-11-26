# Cópia do conteúdo de produção para a homologação

Procedimento executado pelo fundador no **Cloud Shell**, quando quiser a homologação com o
mesmo território, trilhas, catálogo e acervo da produção. Decisão do fundador, 2026-11-26
(documento 03 §1 e documento 09, "Ambiente de homologação"). Produção só é lida.

## O que vai e o que fica

| Vai                                                                                     | Fica em produção                                                   |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| comunidades, locais, pontos de apoio, vínculo do Mestre                                 | Guerreiro(a), responsável e tudo deles — inclusive o portfólio     |
| poderes, trilhas, missões e o conteúdo delas, quiz, coleta, culminância, ODS            | aula, presença, equipe e atividade de aula                         |
| tipos de recurso, preços e valores de referência, catálogo avulso, acervo (patrimônio)  | aporte, livro-razão, ressarcimento, reserva, troca                 |
| desafio extra **aberto**                                                                | desafio extra **direcionado** — leva o nick de uma criança         |
| disciplinas e conteúdos do apoio escolar, texto da vitrine                              | credencial, sessão, chave, auditoria, biometria, termo (semeado)   |
| personas Admin, Mestre e Apoiador, **sem e-mail, WhatsApp e PIN**                       | a persona do fundador — a homologação já tem a dela                |

Sem credencial copiada, os adultos aparecem nas telas mas não entram na homologação. A
lista vive nos dois scripts; tabela que não está nela não sai de produção:

- `2026-11-26-copia-do-conteudo-exportacao.sql` — lê produção numa transação só de leitura e
  já mascara o contato na origem.
- `2026-11-26-copia-do-conteudo-carga.sql` — grava na homologação numa transação única. Uma
  barreira recusa criança, responsável, contato, atividade de aula e desafio direcionado;
  qualquer erro desfaz tudo.

## 1. Preparação

```bash
PROJETO=comunidade-game-506017
REGIAO=southamerica-east1
INSTANCIA=nucleo-db
SEGREDO_DSN_PRODUCAO=<nome do segredo do CG_DSN_BANCO no GCP_SECRETOS_CG de produção>
SEGREDO_DSN_HOMOLOGACAO=$SEGREDO_DSN_PRODUCAO-homologacao
SEGREDO_FUNDADOR=<nome do segredo do CG_IDENTIDADE_FUNDADOR>

mkdir -p ~/copia-hml && cd ~/copia-hml
git clone --depth 1 https://github.com/CarlosSalesNaturalTec/comunidade-game.git repo
# repositório inacessível do Cloud Shell: suba os dois .sql pelo menu "Fazer upload" para
# ~/copia-hml/repo/backend/operacao/
curl -fsSLo cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.18.2/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy
./cloud-sql-proxy --port 5432 $PROJETO:$REGIAO:$INSTANCIA &
```

O _proxy_ autentica pela sua conta e não abre rede autorizada na instância. Se ele recusar
credencial, rode `gcloud auth application-default login` e suba de novo.

A senha sai do DSN guardado no Secret Manager, sem passar pela tela:

```bash
senha() {
  gcloud secrets versions access latest --secret="$1" |
    python3 -c 'import sys, urllib.parse as u; print(u.urlsplit(sys.stdin.read().strip()).password)'
}
PROD="host=127.0.0.1 port=5432 user=comunidade dbname=comunidade_game password=$(senha $SEGREDO_DSN_PRODUCAO)"
HML="host=127.0.0.1 port=5432 user=comunidade_homologacao dbname=comunidade_game_homologacao password=$(senha $SEGREDO_DSN_HOMOLOGACAO)"
```

## 2. Conferências antes da cópia

**Mesmo esquema.** As duas linhas têm de ser idênticas — mesma migração e mesmas colunas na
mesma ordem, que a carga pressupõe. Se divergirem, publique a homologação na versão da
produção antes de seguir.

```bash
ESQUEMA="SELECT (SELECT version_num FROM alembic_version) || ' ' || md5(string_agg(
  table_name || '.' || column_name || '.' || ordinal_position || '.' || data_type, ','
  ORDER BY table_name, ordinal_position))
  FROM information_schema.columns WHERE table_schema = 'public'"
psql "$PROD" -Atc "$ESQUEMA"; psql "$HML" -Atc "$ESQUEMA"
```

**O fundador nos dois ambientes.** Os dois valores têm de vir preenchidos e diferentes:

```bash
IDENTIDADE=$(gcloud secrets versions access latest --secret=$SEGREDO_FUNDADOR)
CREDENCIAL="SELECT persona_id FROM credencial WHERE identificador = :'identidade'"
FP=$(psql "$PROD" -At -v identidade="$IDENTIDADE" <<< "$CREDENCIAL")
FH=$(psql "$HML" -At -v identidade="$IDENTIDADE" <<< "$CREDENCIAL")
echo "produção=$FP homologação=$FH"
```

## 3. Exportação e carga

```bash
psql "$PROD" -q -v fundador=$FP -f repo/backend/operacao/2026-11-26-copia-do-conteudo-exportacao.sql
psql "$HML" -q -1 -v fundador_producao=$FP -v fundador_homologacao=$FH \
  -f repo/backend/operacao/2026-11-26-copia-do-conteudo-carga.sql
```

A carga termina com uma tabela de conferência: `exportadas` e `presentes` iguais em toda
linha. Ela é **idempotente pelo id** — rodar de novo pula o que já entrou e só regrava o
texto da vitrine.

Se parar com `duplicate key ... uq_<tabela>_<coluna>`, um dado sintético da homologação tem
o mesmo nome de um de produção (poder, disciplina...). Nada foi gravado: renomeie ou apague
o sintético e rode a carga de novo. Erro de chave estrangeira para `persona` quer dizer que
um conteúdo copiado aponta para criança ou responsável — pare e investigue, não force.

## 4. Arquivos do conteúdo

Só o prefixo `conteudos/`, que guarda os arquivos das missões. Os demais prefixos do bucket
(aportes, comprovantes, ressarcimentos, customizações) são movimento ou portfólio e ficam.

```bash
gcloud storage rsync --recursive gs://comunidade-game-armazenamento/conteudos \
  gs://comunidade-game-armazenamento-homologacao/conteudos
```

## 5. Encerramento

```bash
kill %1
cd ~ && rm -rf ~/copia-hml
```

Os CSVs não têm contato, mas têm nomes de adultos reais: não ficam no Cloud Shell.

Conferência final: na homologação, uma trilha de produção abre com o conteúdo e os
arquivos na App 01.
