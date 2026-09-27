import { Cabecalho } from "comum/react";
import { useState } from "react";
import { DialogoDeEntrada } from "./entrada/DialogoDeEntrada";
import { NavegacaoDeRecortes } from "./navegacao/NavegacaoDeRecortes";
import { recorteDoCaminho } from "./navegacao/recortes";
import { useNavegacao } from "./navegacao/useNavegacao";
import { TelaDoRecorte } from "./recortes/TelaDoRecorte";

// A vitrine não monta `ProvedorDeSessao` nem `ProvedorDeNarracao`: o primeiro
// guarda sessão e o segundo guarda a preferência do aparelho, e aqui nada do
// visitante é guardado (`RF-03-51`, `RN-03-01`, `RN-03-22`). Sem provedor, a
// camada de narração fica inerte por construção.
export default function App() {
  const { caminho, irPara } = useNavegacao();
  const [entradaAberta, definirEntradaAberta] = useState(false);
  const recorte = recorteDoCaminho(caminho);

  return (
    <>
      {/* O "Entrar" fica no cabeçalho, presente em toda tela pública
          (`RF-03-58`). */}
      <Cabecalho
        titulo="Comunidade Game"
        subtitulo="A vitrine pública do projeto — aberta, sem cadastro e sem login."
        acao={{ rotulo: "Entrar", aoAcionar: () => definirEntradaAberta(true) }}
      />
      <NavegacaoDeRecortes recorteAtual={recorte.chave} aoSelecionarRecorte={irPara} />
      <TelaDoRecorte recorte={recorte} />
      <DialogoDeEntrada aberto={entradaAberta} aoFechar={() => definirEntradaAberta(false)} />
    </>
  );
}
