"""Registro único dos modelos do núcleo.

Importar este módulo popula `Base.metadata` com **todas** as tabelas. Todo
ponto de entrada que fale com o banco fora das rotas — o `cli.py` da
implantação e o `env.py` do Alembic — importa daqui, em vez de refazer a
lista à mão: modelo esquecido vira chave estrangeira sem tabela de destino,
e o erro só aparece no primeiro `commit` em produção.

A aplicação não precisa dele: `principal.py` alcança os mesmos modelos ao
importar os roteadores.
"""

from .apoio_escolar import modelo as _modelo_apoio_escolar  # noqa: F401
from .aportes import modelo as _modelo_aportes  # noqa: F401
from .auditoria import modelo as _modelo_auditoria  # noqa: F401
from .aulas import modelo as _modelo_aulas  # noqa: F401
from .biometria import modelo as _modelo_biometria  # noqa: F401
from .catalogo_avulso import modelo as _modelo_catalogo_avulso  # noqa: F401
from .chaves import modelo as _modelo_chaves  # noqa: F401
from .coletas import modelo as _modelo_coletas  # noqa: F401
from .comunidades import modelo as _modelo_comunidades  # noqa: F401
from .consentimentos import modelo as _modelo_consentimentos  # noqa: F401
from .criacoes_originais import modelo as _modelo_criacoes_originais  # noqa: F401
from .culminancias import modelo as _modelo_culminancias  # noqa: F401
from .equipes import modelo as _modelo_equipes  # noqa: F401
from .fila import modelo as _modelo_fila  # noqa: F401
from .livro_razao import modelo as _modelo_livro_razao  # noqa: F401
from .locais import modelo as _modelo_locais  # noqa: F401
from .ocorrencias_de_conduta import modelo as _modelo_ocorrencias_de_conduta  # noqa: F401
from .ods import modelo as _modelo_ods  # noqa: F401
from .patrimonio import modelo as _modelo_patrimonio  # noqa: F401
from .personas import modelo as _modelo_personas  # noqa: F401
from .poderes import modelo as _modelo_poderes  # noqa: F401
from .ponto_extra import modelo as _modelo_ponto_extra  # noqa: F401
from .pontos_de_apoio import modelo as _modelo_pontos_de_apoio  # noqa: F401
from .pontuacao import modelo as _modelo_pontuacao  # noqa: F401
from .quiz import modelo as _modelo_quiz  # noqa: F401
from .recompensas_de_marco import modelo as _modelo_recompensas_de_marco  # noqa: F401
from .recursos import modelo as _modelo_recursos  # noqa: F401
from .reservas import modelo as _modelo_reservas  # noqa: F401
from .responsaveis import modelo as _modelo_responsaveis  # noqa: F401
from .ressarcimentos import modelo as _modelo_ressarcimentos  # noqa: F401
from .resultados import modelo as _modelo_resultados  # noqa: F401
from .sessoes import modelo as _modelo_sessoes  # noqa: F401
from .trilhas import modelo as _modelo_trilhas  # noqa: F401
from .trocas import modelo as _modelo_trocas  # noqa: F401
