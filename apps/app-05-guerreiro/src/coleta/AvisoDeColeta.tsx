import { useState } from "react";

// Aviso discreto nas telas que coletam dado da criança, com acesso à área
// detalhada — nunca bloqueia a tela nem exige confirmação para continuar
// (`RF-05-57`, documento 03 §12).
export function AvisoDeColeta() {
  const [aberto, definirAberto] = useState(false);

  return (
    <div className="cg-aviso-de-coleta">
      <p>
        Esta tela guarda o valor que você mede, a data e o local do território.{" "}
        <button
          type="button"
          className="cg-aviso-de-coleta__botao"
          aria-expanded={aberto}
          onClick={() => definirAberto((valor) => !valor)}
        >
          {aberto ? "Ver menos" : "Saber mais"}
        </button>
      </p>
      {aberto && (
        <p className="cg-aviso-de-coleta__detalhe">
          Esse dado do território fica guardado com o seu nome de coletor(a), para valer a sua
          conquista. Quando ele aparece em painéis ou pesquisas, ninguém descobre quem mediu —
          só o valor e o lugar aparecem.
        </p>
      )}
    </div>
  );
}
