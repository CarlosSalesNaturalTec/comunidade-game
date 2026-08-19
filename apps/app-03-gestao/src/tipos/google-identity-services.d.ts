export {};

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize(opcoes: {
            client_id: string;
            callback: (resposta: { credential: string }) => void;
          }): void;
          renderButton(elemento: HTMLElement, opcoes: { theme: string; size: string }): void;
        };
      };
    };
  }
}
