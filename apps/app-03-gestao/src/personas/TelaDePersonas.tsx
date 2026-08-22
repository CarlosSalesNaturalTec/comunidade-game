import { Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { FormularioDeAdmin } from "./FormularioDeAdmin";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { TelaDeAdultos } from "./TelaDeAdultos";
import { TelaDeGuerreiros } from "./TelaDeGuerreiros";

type SubArea = "guerreiros" | "mestres" | "apoiadores" | "admins" | "responsaveis";

const SUB_AREAS: { chave: SubArea; rotulo: string }[] = [
  { chave: "guerreiros", rotulo: "Guerreiros e Guerreiras" },
  { chave: "mestres", rotulo: "Mestres" },
  { chave: "apoiadores", rotulo: "Apoiadores" },
  { chave: "admins", rotulo: "Admins" },
  { chave: "responsaveis", rotulo: "Responsáveis" },
];

export function TelaDePersonas() {
  const { sair } = useSessao();
  const [subArea, definirSubArea] = useState<SubArea>("guerreiros");
  const [mostrarFormularioDeAdmin, definirMostrarFormularioDeAdmin] = useState(false);
  const [mostrarFormularioDeResponsavel, definirMostrarFormularioDeResponsavel] =
    useState(false);

  return (
    <Moldura>
      <Cabecalho titulo="Personas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      <nav className="cg-navegacao" aria-label="Tipos de persona">
        {SUB_AREAS.map((item) => (
          <button
            key={item.chave}
            type="button"
            className="cg-navegacao__item"
            aria-current={subArea === item.chave || undefined}
            onClick={() => definirSubArea(item.chave)}
          >
            {item.rotulo}
          </button>
        ))}
      </nav>

      {subArea === "guerreiros" && <TelaDeGuerreiros />}
      {subArea === "mestres" && <TelaDeAdultos papel="mestre" />}
      {subArea === "apoiadores" && <TelaDeAdultos papel="apoiador" />}

      {subArea === "admins" &&
        (mostrarFormularioDeAdmin ? (
          <FormularioDeAdmin
            onSalvo={() => definirMostrarFormularioDeAdmin(false)}
            onCancelar={() => definirMostrarFormularioDeAdmin(false)}
          />
        ) : (
          <Botao onClick={() => definirMostrarFormularioDeAdmin(true)}>Incluir Admin</Botao>
        ))}

      {subArea === "responsaveis" &&
        (mostrarFormularioDeResponsavel ? (
          <FormularioDeResponsavel
            onConcluido={() => definirMostrarFormularioDeResponsavel(false)}
            onCancelar={() => definirMostrarFormularioDeResponsavel(false)}
          />
        ) : (
          <Botao onClick={() => definirMostrarFormularioDeResponsavel(true)}>
            Cadastrar responsável
          </Botao>
        ))}
    </Moldura>
  );
}
