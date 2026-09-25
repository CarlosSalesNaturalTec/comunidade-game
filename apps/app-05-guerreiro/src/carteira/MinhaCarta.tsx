import { CartaDoGuerreiro } from "comum/carta";

// A carta do próprio Guerreiro(a) na Área dele (`RF-05-50`, `RF-05-51`,
// documento 11 §8.2). A montagem foi promovida a `comum/carta` quando a App 01
// passou a apresentar a mesma carta no desfecho da presença (decisão do
// fundador de 2026-09-25); aqui fica só a frase desta aplicação para quando a
// leitura não trouxer tudo o que a variante exige.
const AVISO_DA_CARTA_INCOMPLETA =
  "A sua carta aparece aqui quando o seu percurso tiver tudo o que ela mostra — avatar, " +
  "apelido, poderes, badges e criações. Suas conquistas seguem nas abas abaixo.";

export function MinhaCarta() {
  return <CartaDoGuerreiro aviso={AVISO_DA_CARTA_INCOMPLETA} />;
}
