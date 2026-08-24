import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import type { GuerreiroCadastrado } from "../api/guerreiros";
import { existeCamera } from "../biometria/biometria";
import { TelaDeCadastro } from "./TelaDeCadastro";
import { TelaDeCaptura } from "./TelaDeCaptura";
import { TelaDoResponsavel } from "./TelaDoResponsavel";
import { TelaDoTermo } from "./TelaDoTermo";

interface Props {
  tokenDeTrabalho: string;
  personaIdDeTrabalho: string;
  aulaId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
}

type Passo =
  | { tipo: "guerreiro" }
  | { tipo: "sem_camera" }
  | { tipo: "responsavel"; guerreiro: GuerreiroCadastrado }
  | { tipo: "termo"; guerreiro: GuerreiroCadastrado; responsavelId: string }
  | { tipo: "captura"; guerreiro: GuerreiroCadastrado };

// A cadeia de cinco chamadas HTTP da jornada 5.2, retomável por passo
// concluído (design — decisão 4): cada passo só avança depois do anterior
// gravar, e nenhum estado parcial é inválido — o pior desfecho, parar em
// qualquer ponto depois do cadastro do Guerreiro(a), já é a jornada 5.3
// (`RF-04-04`, `RF-04-15`, `RN-04-03`, `RN-04-09`).
export function FluxoDeOnboarding({
  tokenDeTrabalho,
  personaIdDeTrabalho,
  aulaId,
  aoConcluir,
  aoVoltar,
}: Props) {
  const [passo, definirPasso] = useState<Passo>({ tipo: "guerreiro" });

  // A câmera é conferida uma vez, logo depois do cadastro do Guerreiro(a):
  // sem ela, o caminho do responsável e do termo não fazem sentido — o
  // cadastro já está completo pela jornada 5.3 (design — decisão 6).
  async function aoCadastrarGuerreiro(guerreiro: GuerreiroCadastrado) {
    const temCamera = await existeCamera();
    definirPasso(temCamera ? { tipo: "responsavel", guerreiro } : { tipo: "sem_camera" });
  }

  if (passo.tipo === "guerreiro") {
    return (
      <TelaDeCadastro
        tokenDeTrabalho={tokenDeTrabalho}
        aulaId={aulaId}
        aoConcluir={aoCadastrarGuerreiro}
        aoVoltar={aoVoltar}
      />
    );
  }

  if (passo.tipo === "sem_camera") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Cadastro concluído"
          acao={{ rotulo: "Voltar ao início", aoAcionar: aoConcluir }}
        />
        <Aviso tipo="atencao">
          Este aparelho não tem câmera. O cadastro foi concluído e o Guerreiro(a) já participa
          da aula; a captura da imagem exige um aparelho com câmera.
        </Aviso>
        <Botao onClick={aoConcluir}>Concluir</Botao>
      </Moldura>
    );
  }

  if (passo.tipo === "responsavel") {
    return (
      <TelaDoResponsavel
        tokenDeTrabalho={tokenDeTrabalho}
        guerreiroId={passo.guerreiro.id}
        aoConcluir={(responsavelId) =>
          definirPasso({ tipo: "termo", guerreiro: passo.guerreiro, responsavelId })
        }
        aoVoltar={aoConcluir}
      />
    );
  }

  if (passo.tipo === "termo") {
    return (
      <TelaDoTermo
        tokenDeTrabalho={tokenDeTrabalho}
        personaIdDeTrabalho={personaIdDeTrabalho}
        responsavelId={passo.responsavelId}
        guerreiroId={passo.guerreiro.id}
        aoConcluir={() => definirPasso({ tipo: "captura", guerreiro: passo.guerreiro })}
        aoVoltar={aoConcluir}
      />
    );
  }

  return (
    <TelaDeCaptura
      tokenDeTrabalho={tokenDeTrabalho}
      guerreiroId={passo.guerreiro.id}
      aoConcluir={aoConcluir}
      aoVoltar={aoConcluir}
    />
  );
}
