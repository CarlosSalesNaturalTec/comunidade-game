import { BotaoDeEntradaGoogle } from "./BotaoDeEntradaGoogle";
import { useSessao } from "./ContextoDeSessao";

export function TelaDeEntrada() {
  const { entrarComGoogle, entrando, erroDeEntrada } = useSessao();

  return (
    <main className="tela-de-entrada">
      <h1>Comunidade Game — Gestão</h1>
      <p>Entre com a conta Google vinculada ao seu cadastro.</p>
      <BotaoDeEntradaGoogle aoReceberIdToken={entrarComGoogle} />
      {entrando && <p role="status">Entrando…</p>}
      {erroDeEntrada && <p role="alert">{erroDeEntrada}</p>}
    </main>
  );
}
