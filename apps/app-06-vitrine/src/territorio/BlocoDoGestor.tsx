// O **bloco em destaque** que abre o recorte de gestores públicos, antes do
// painel (`RF-03-63`): o que a plataforma produz e para que serve, com usos
// concretos e o caminho do conjunto completo (`RF-03-64`), e os dois limites
// declarados — dado agregado, nunca por Guerreiro(a), e que não substitui
// indicador oficial (`RF-03-65`, `RN-03-28`).
//
// Os usos concretos são os do PRD-03 §5.3, que os nomeia: resíduos,
// iluminação, buracos na via, transporte, defesa civil e escolas.
export function BlocoDoGestor() {
  return (
    <div className="cg-bloco-do-gestor">
      <p>
        A plataforma produz <strong>séries históricas do território</strong> medidas por
        moradores: crianças e jovens registram o que acontece no lugar onde vivem, em cadência
        declarada, com a origem de cada medição gravada.
      </p>
      <p>Para que serve, na prática:</p>
      <ul>
        <li>Resíduos acumulados e pontos de descarte irregular</li>
        <li>Iluminação pública apagada</li>
        <li>Buracos na via e conservação do calçamento</li>
        <li>Transporte e deslocamento</li>
        <li>Defesa civil: chuva, alagamento e risco</li>
        <li>Escolas e equipamentos públicos do entorno</li>
      </ul>
      <p>
        <strong>Como pedir o conjunto completo:</strong> pelo formulário de solicitação de
        dados da vitrine. A entrega é gratuita e anonimizada, e sai depois da aprovação de um
        Admin — não há entrega automática.
      </p>
      <p>
        <strong>Como apoiar e como replicar:</strong> o apoio entra pela seção "Como apoiar", e
        o código é aberto — outra comunidade pode replicar o modelo inteiro.
      </p>
      <p className="cg-bloco-do-gestor__limites">
        <strong>Limites deste dado.</strong> Ele é <strong>agregado e anonimizado</strong>, e
        nunca sai por Guerreiro(a): o painel para no bairro e não identifica quem coletou. E
        ele <strong>não substitui indicador oficial</strong> — é evidência produzida por
        moradores sobre o próprio lugar.
      </p>
    </div>
  );
}
