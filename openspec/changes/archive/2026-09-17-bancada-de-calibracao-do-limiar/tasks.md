## 1. A distância no aparelho, igual à do núcleo

- [x] 1.1 Expor em `comum/biometria` a função que calcula a distância euclidiana entre dois
      descritores, no mesmo cálculo de `_distancia_euclidiana` do núcleo — raiz da soma dos
      quadrados, sobre o descritor cru (`RF-04-63`, design — decisão 1).
- [x] 1.2 Cobrir em `comum/biometria` a função com **valores fixos conhecidos**, cujos
      resultados estão escritos no teste: é o que prende as duas implementações e faz a
      divergência aparecer no CI em vez de no encontro (`RF-04-63`, design — Riscos).

## 2. A tela de medição

- [x] 2.1 Criar em `apps/app-01-aula-presencial/` a tela que captura pela `comum/biometria`,
      guarda **um** descritor de referência por vez, compara cada captura seguinte com ele,
      apresenta a distância e descarta a captura comparada no mesmo ato — sem nunca apresentar
      nem persistir descritor, e sem nenhuma chamada ao núcleo (`RF-04-63`, `RN-04-32`).
- [x] 2.2 Dar à tela a substituição explícita da referência, como ato de quem opera, e encerrar
      a câmera ao sair, como a `TelaDeCaptura` já faz (`RN-04-32`, `RN-04-12`, design —
      decisão 2).
- [x] 2.3 Ligar os dois caminhos com alcance diferente: pela tela inicial, em sessão de trabalho
      de Mestre ou Admin, medindo **apenas quem opera**; e pelo passo da imagem do
      `FluxoDeOnboarding`, depois do termo, medindo **o Guerreiro(a) daquele cadastro**
      (`RN-04-33`, `RN-04-07`, design — decisões 3 e 4).
- [x] 2.4 Cobrir em teste da App 01 os cinco cenários do delta: a distância apresentada; só um
      descritor de referência guardado ao longo de três capturas; nenhuma requisição ao núcleo
      durante a medição; fora do onboarding não há caminho que capture Guerreiro(a); e dentro
      do onboarding a medição é oferecida depois do consentimento (`RF-04-63`, `RN-04-32`,
      `RN-04-33`).

## 3. O aviso de coleta

- [x] 3.1 Acrescentar a medição à área detalhada de direitos
      (`AreaDetalhadaDeDireitos.tsx`) — que ela abre a câmera, compara no aparelho, descarta no
      ato, não envia nada, e sobre Guerreiro(a) só acontece sob o termo assinado —, cobrindo em
      `direitos.test.tsx` o cenário correspondente do delta (`RF-04-26`, `RF-04-63`).

## 4. Implantação

- [ ] 4.1 **EM ABERTO — exige acesso ao Secret Manager, que a sessão de implementação não
      tem.** Medir no aparelho, escolher o limiar confortavelmente abaixo do menor valor entre
      pessoas diferentes e acima do maior da mesma pessoa, e gravá-lo no secret
      `cg-biometria-limiar-de-comparacao`, hoje em `0.5`. Na dúvida, apertado: recusar criança
      legítima custa uma confirmação do Mestre; aceitar a errada não se desfaz (documento 09,
      "Parâmetros da entrada do Guerreiro(a)"). Anexar os números à change.

      A **primeira medição não depende de encontro real**, ao contrário do que esta tarefa
      dizia quando foi escrita: o caminho do diagnóstico, da tela inicial, mede **quem opera**,
      e dois adultos no mesmo aparelho já dão o piso (mesma pessoa em capturas sucessivas) e o
      teto (pessoas diferentes). O encontro real serve para **conferir com rosto de criança** e
      ajustar se divergir — não para começar. Corrigido depois do teste em produção de
      2026-09-17, que confirmou a captura gravando e a entrada recusando com o limiar em `0.5`.

## 5. Documentação

- [x] 5.1 Marcar como implementada a **fatia 14** no bloco do PRD-04 do
      `openspec/cronograma-de-fatias.md`, acrescentada com situação `em andamento` na abertura,
      com a ressalva da tarefa 4.1 enquanto o limiar não tiver sido medido e gravado. Nada muda
      em `docs/`: a decisão nova já está no documento 03 §3.3, no documento 09 §1 e no PRD-04,
      pelo PR de revisão do PRD que esta change pressupõe. `docs/prds/index.md` e o documento 99
      não mudam.
