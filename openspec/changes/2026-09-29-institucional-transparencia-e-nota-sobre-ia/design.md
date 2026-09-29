## Context

Fatia de núcleo e de tela. O núcleo não tem a entidade nem a rota (PRD-03 §9 e PRD-02 §9 as
declaram, e o cronograma manda a fatia 5 levá-las). Padrões que já existem e se reaproveitam: a
leitura pública sob `/v1/vitrine` com chave e sem persona (`leitura-publica-da-vitrine`); a
semeadura idempotente da implantação (`termos/semeadura.py`, chamada por `cli.semear`); a
operação de matriz sem papel próprio, que só o Admin alcança por `Operacao.tudo`
(`catalogo_de_poderes`); a auditoria de toda escrita pelo `MiddlewareDeAuditoria`; e, na App 06,
a seção por recorte (`navegacao/recortes.ts`), o endereço próprio e a ausência de rastro
(`aplicacao-da-vitrine`). Nenhuma decisão de produto nova: a chave PIX é do documento 04 §1, a
nota e o bloco "Licenças" dentro de "Quem somos" são do documento 03 §8 e do 09, e as três
escolhas de forma abaixo foram confirmadas pelo fundador em 2026-09-29.

## Decisions

1. **Uma tabela, três linhas, chave natural `secao`** (`quem-somos`, `contatos`, `como-apoiar`),
   com `texto`, `video_url`, `publicado_em` e `autor_id` — **nulo** quando quem gravou foi a
   semeadura, que não tem persona. Sem histórico de versões: a trilha de auditoria já guarda cada
   escrita (`RF-01-29`). A linha nasce na primeira publicação ou semeadura; a leitura completa as
   ausentes, e a resposta tem sempre as três, em ordem fixa. Alternativa descartada: quatro
   linhas, com a nota à parte — a nota vive **dentro** de "Quem somos" (doc 03 §8) e o `PUT` do
   PRD-02 fala em três seções.
2. **Escrita no núcleo.** `PUT /v1/conteudo-institucional/{secao}` de Admin sai com o `GET`, com
   o corpo `{texto, video_url?}`. O `PUT` devolve autor e data; o público nunca vê o autor. A
   leitura de Admin com autor, para a tela de edição, é da fatia 16 do PRD-02. Operação nova
   `conteudo_institucional`, sem entrada na matriz de ninguém (precedente `catalogo_de_poderes`).
3. **PIX e vídeo dentro das seções, sem atributo próprio da chave.** A chave PIX e o titular são
   **texto** de "Como apoiar", semeado do documento 04 §1 e editável pelo Admin: a aplicação não
   escreve valor nenhum. O vídeo é o **único campo extra**, `video_url`, aceito só em "Quem
   somos", `https`, opcional. Alternativa descartada: colunas `chave_pix` e `titular` — criam
   atributo que o PRD não lista.
4. **Formato do texto: parágrafos e `## Título`.** Uma linha `## ` abre um bloco com título, cujo
   `id` na tela é o título sem acento e em minúscula com hífen (`nota-de-transparencia-sobre-ia`,
   `licencas`). É a única marcação. O texto entra na tela como texto do React, nunca como HTML.
   Alternativas descartadas: Markdown ou HTML — pedem sanitizador e dependência nova, para um
   texto que só precisa de parágrafo e título. O endereço estável da nota é
   `/#nota-de-transparencia-sobre-ia`: a tela rola até o bloco quando o conteúdo chega.
5. **Vídeo como link, não como player.** Embutir o player de uma plataforma de vídeo carrega
   recurso e cookie de terceiro na abertura da página, contra `RF-03-51`, `RN-03-22` e o
   princípio 6 do documento 15. A tela oferece o acesso e o visitante decide sair. O
   `RF-03-49` é desejável, e onde o vídeo fica hospedado é insumo do fundador.
6. **Semeadura só onde a seção não tem texto**, em `conteudo_institucional/semeadura.py`,
   chamada por `cli.semear`. "Como apoiar" recebe a chave PIX e o titular; "Quem somos" recebe o
   rascunho abaixo; "Contatos" fica **vazio** — nenhum documento traz os contatos, e inventá-los
   seria regra. A semeadura nunca sobrescreve uma publicação.
7. **Uma leitura por carga de página**, guardada só em memória (uma promessa no módulo, que morre na recarga), compartilhada pelas três seções.
   O visitante não ganha nada no aparelho (`RN-03-22`); o cache HTTP não é desenhado aqui — o
   núcleo não tem padrão de cabeçalho de cache, e é decisão de infraestrutura.
8. **Aviso de coleta em `App.tsx`**, fora do recorte, para valer em toda tela sem depender de
   cada uma. É uma linha discreta ao pé, com o botão que leva a `/o-que-coletamos`. A **área
   detalhada** é conteúdo estático da aplicação, no mesmo espírito de `direitos/` da App 09,
   derivada da tabela do PRD-03 §11 e da §12.2 do documento 03, **sem número que esses dois não
   tragam**. Não é editável pelo Admin: o PRD-02 só edita as três seções.
9. **Ordem nos recortes.** Em "sociedade civil", "Quem somos" **abre** (o PRD-03 §5.1 põe a
   narrativa e o vídeo antes dos cards) e "Como apoiar" e "Contatos" fecham; "Contatos" entra
   também no fim de "pesquisadores" e de "gestores públicos". "Como apoiar" segue com a frase de
   que as necessidades em aberto chegam em entrega própria, até a fatia 6.

### Rascunho semeado em "Quem somos"

Para revisão do fundador antes do merge; segue o documento 01 §7 (o que a nota pública diz) e o
documento 03 §§1.12 e 8.

```text
## Nota de transparência sobre IA

A Comunidade Game usa inteligência artificial e diz isso às claras.

Para construir a plataforma — o código e os documentos —, usamos os modelos Claude 5 e Sonnet
5, da Anthropic.

Para atender as pessoas na tela — Guerreiros, Guerreiras, Mestres e Apoiadores —, usamos modelos
de terceiros: hoje o Gemini, do Google, e o DeepSeek. Quem constrói não é quem responde a uma
criança.

A IA reescreve o conteúdo que o Mestre cadastrou, para a criança entender melhor, dentro da
conversa do momento. Ela não faz perfil da criança: nada é adivinhado nem guardado sobre quem
ela é. O texto reescrito por IA leva uma etiqueta visível, com link para esta nota.

A voz que lê as telas em voz alta é a do próprio navegador. Ela lê texto da plataforma, nunca o
nome de uma criança.

Sobre o que é gerado com auxílio de IA, veja o bloco Licenças, logo abaixo.

## Licenças

O código da plataforma é aberto, sob a licença AGPL. O conteúdo educacional publicado, com
crédito ao Mestre autor, e o conjunto de dados entregue a pesquisadores e gestores, com crédito
à comunidade que o produziu, saem sob a licença CC BY-SA: quem usa pode adaptar, creditando, e o
derivado herda a mesma licença.
```

Semente de "Como apoiar" (documento 04 §1): "Doações em dinheiro são feitas por PIX, em nome da
pessoa jurídica vinculada ao projeto", a chave `51.730.395/0001-19` (CNPJ), o titular "Robô Educa
— Kits Robóticos Educacionais" e a frase de que toda doação recebida é registrada no livro-razão.

## Risks / Trade-offs

- [O texto da nota é jurídico e público] → é rascunho até o fundador aprovar; entra pela
  semeadura, e o Admin o troca por `PUT` sem nova implantação.
- [Divergência de fonte: o documento 09 diz só Gemini no atendimento; os documentos 01 §7 e
  03 §1.12 dizem Gemini e DeepSeek, decisão de 2026-09-10] → o rascunho segue os dois documentos
  de cima, e a linha do documento 09 é ajustada na tarefa de documentação.
- [Aviso de coleta em toda tela pode virar ruído] → uma linha, sem bloqueio nem confirmação
  (documento 03 §12: "discreta e elegante, sem interromper o uso").
- [A fatia 6 precisa da chave PIX na porta do pré-cadastro] → lê a mesma seção "Como apoiar" pelo
  hook compartilhado; nada a guardar de novo.
- [A tela de edição da fatia 16 precisa do autor e da data ao abrir] → o `PUT` os devolve, e a
  leitura de Admin é decisão daquela fatia, que o PRD-02 §9 ainda não lista.

## Migration Plan

Migração Alembic cria a tabela vazia; `semear` a preenche nas duas seções, na implantação.
Reversão: a migração desce e apaga a tabela — nenhum outro dado depende dela.

## Open Questions

- O que o bloco "Licenças" diz sobre o **gerado com auxílio de IA**. Nenhum documento fixa a
  regra, e o rascunho não a afirma: a nota só remete ao bloco, que fala das três licenças
  decididas. O fundador completa o texto na revisão; não muda o desenho nem as tarefas.
