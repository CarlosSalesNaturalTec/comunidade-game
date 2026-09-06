import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";
import "@testing-library/jest-dom/vitest";

afterEach(() => {
  cleanup();
});

// jsdom não implementa `HTMLDialogElement.showModal`/`close` (design —
// Risks): sem isso o teste do `Dialogo` falharia por ambiente, não por
// comportamento. O polyfill reproduz o que o navegador já faz de graça —
// foco preso ao `Tab` e fechamento por `Esc` —, para o componente
// continuar sem reimplementar isso (design — decisão 3).
if (typeof HTMLDialogElement !== "undefined" && !HTMLDialogElement.prototype.showModal) {
  function elementosFocaveis(dialogo: HTMLDialogElement): HTMLElement[] {
    return Array.from(
      dialogo.querySelectorAll<HTMLElement>(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
      ),
    );
  }

  function aoTeclar(evento: KeyboardEvent) {
    const dialogo = document.querySelector<HTMLDialogElement>("dialog[open]");
    if (!dialogo) return;

    if (evento.key === "Escape") {
      evento.preventDefault();
      dialogo.close();
      return;
    }

    if (evento.key !== "Tab") return;
    const focaveis = elementosFocaveis(dialogo);
    if (focaveis.length === 0) return;

    const primeiro = focaveis[0];
    const ultimo = focaveis[focaveis.length - 1];
    const atual = document.activeElement;

    if (evento.shiftKey && atual === primeiro) {
      evento.preventDefault();
      ultimo.focus();
    } else if (!evento.shiftKey && atual === ultimo) {
      evento.preventDefault();
      primeiro.focus();
    } else if (!dialogo.contains(atual)) {
      evento.preventDefault();
      primeiro.focus();
    }
  }

  document.addEventListener("keydown", aoTeclar);

  HTMLDialogElement.prototype.showModal = function showModal(this: HTMLDialogElement) {
    this.setAttribute("open", "");
    elementosFocaveis(this)[0]?.focus();
  };

  HTMLDialogElement.prototype.close = function close(this: HTMLDialogElement) {
    if (!this.hasAttribute("open")) return;
    this.removeAttribute("open");
    this.dispatchEvent(new Event("close"));
  };
}
