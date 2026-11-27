# Can Machines Fool Humans?

API de um experimento educacional sobre conversas em inglês. Python 3.11+, FastAPI, SQLAlchemy, SQLite, NLTK e SDK oficial Google Gen AI.

## Perguntas de pesquisa

- How does prompt engineering influence an artificial intelligence system's ability to imitate human conversation?
- How has the ability of machines to imitate human conversation evolved from ELIZA to modern large language models?

Em [Computing Machinery and Intelligence (1950)](https://doi.org/10.1093/mind/LIX.236.433), Alan Turing propôs o *Imitation Game*, em que um julgador usa conversas escritas para distinguir interlocutores. Este projeto adapta a ideia para medir a similaridade percebida com uma conversa humana. Todos os interlocutores são artificiais. A atividade não reproduz integralmente o jogo original, que inclui interlocutores humanos.

Joseph Weizenbaum apresentou [ELIZA em 1966](https://doi.org/10.1145/365153.365168). O grupo A usa a [recriação do NLTK](https://www.nltk.org/api/nltk.chat.eliza.html), que usa expressões regulares, reflexões de pronomes e respostas predefinidas, sem redes neurais. O código histórico de 1966 é distinto da recriação. O Gemini gera texto com um modelo de linguagem moderno que usa o histórico da conversa como contexto.

Prompt Engineering consiste em alterar as instruções fornecidas ao modelo para influenciar o resultado. O *zero-shot* define o comportamento esperado. O *few-shot* também fornece exemplos de conversa que demonstram o estilo esperado.

## Metodologia

| Grupo | Condição |
|---|---|
| A | ELIZA local |
| B | Gemini Baseline com a instrução mínima em inglês |
| C | Gemini Zero-shot com instruções sobre o estilo da conversa |
| D | Gemini Few-shot com as instruções de C e exemplos de estilo |

Hipóteses a avaliar com os dados coletados:

- **H1.** Gemini será percebido como humano com maior frequência que ELIZA.
- **H2.** Gemini com Prompt Engineering será percebido como humano com maior frequência que Gemini Baseline.
- **H3.** Exemplos de conversa e personas podem aumentar a naturalidade percebida. A comparação D × C avalia os exemplos no contexto das mesmas instruções de atuação. O desenho atual não estima um efeito independente de persona.

A variável independente é a condição. Entre B, C e D, o modelo, a temperatura, o top-p, o limite de tokens de saída, o número de candidatos e os limites de conversa são iguais. Cada chamada envia a conversa inteira daquela sessão, dentro dos limites de mensagens e caracteres. O modelo define o tamanho da janela de contexto. As variáveis dependentes são a classificação, a confiança e as notas de naturalidade, coerência e compreensão emocional percebida. Latência e tokens são métricas operacionais. O backend escolhe aleatoriamente entre os grupos disponíveis com menor número de sessões iniciadas. A condição, os limites, os parâmetros de geração e a versão de prompt ficam vinculados à sessão.

Antes de iniciar, mostre o aviso e a disponibilidade retornados por `GET /health` com o prefixo da API. O participante confirma a ciência do aviso e conversa em inglês. O UUID da sessão dá acesso ao histórico e aos demais endpoints daquela sessão. Trate-o como credencial. O backend oculta os metadados da condição até a avaliação e a revelação. A avaliação pode ser enviada uma vez. Com o limite padrão, a décima resposta encerra a conversa automaticamente. É possível encerrar antes, após ao menos uma resposta. O backend registra as duas mensagens de um turno juntas após obter a resposta.

A **Human Perception Rate** é o número de classificações como humanas dividido pelo total de avaliações válidas, em escala de 0 a 1. O relatório também inclui os percentuais por classificação e as diferenças absolutas contra B em pontos percentuais. Uma sessão concluída é uma conversa encerrada, inclusive se a avaliação estiver pendente. Latência média e mediana e médias de tokens usam respostas de conversas concluídas com o respectivo dado disponível. Latência mede o tempo observado no backend. Valores ausentes retornam como `null`. Os resultados são descritivos, sem limiar de aprovação. O CSV inclui uma linha por conversa concluída e omite UUIDs, transcrições, comentários e horários. Comentários opcionais ficam no SQLite para análise local.

### Limitações

A divulgação de que todos conversam com chatbots pode afetar a classificação. Estilo, latência percebida e respostas espontâneas sobre a própria identidade também podem dar pistas. As notas são subjetivas e o texto em inglês é solicitado ao participante e instruído no prompt do Gemini, sem filtro de idioma. Compare amostras coletadas sob a mesma configuração de modelo, versão dos prompts e limites. Use um arquivo de banco novo por rodada se alterar essas condições, para evitar misturar configurações no relatório agregado. Uma fase só com ELIZA impede comparações entre grupos até haver avaliações nos demais. A disponibilidade indica a presença de configuração, pois a primeira verificação contra o provedor ocorre no envio de uma mensagem.

## Arquitetura

- `app/main.py` configura a aplicação, CORS, exceções e o ciclo de vida.
- `app/routers/` implementa a API e autentica endpoints administrativos.
- `app/schemas/` valida entradas e define os campos públicos.
- `app/services/` executa o protocolo, integra ELIZA e Gemini, versiona prompts e calcula métricas.
- `app/database/` contém entidades SQLAlchemy, conexão SQLite e consultas de sessão.
- `app/prompts/` contém baseline, zero-shot e demonstrações few-shot. O conteúdo exato enviado recebe um SHA-256, é armazenado no banco e mantém o histórico quando os arquivos mudam.
- `tests/` contém testes HTTP com SQLite temporário e chamadas ao Gemini simuladas.

## Instalação e execução

No Windows (PowerShell), a partir da raiz do projeto, com o ambiente existente:

```powershell
cd backend
Copy-Item .env.example .env
..\venv\Scripts\python.exe -m pip install -r requirements.txt
..\venv\Scripts\python.exe -m uvicorn app.main:app
```

Para criar o ambiente na raiz antes desses comandos, use `py -3.12 -m venv venv`.

No Linux, a partir da raiz:

```bash
python3 -m venv venv
cd backend
cp .env.example .env
../venv/bin/python -m pip install -r requirements.txt
../venv/bin/python -m uvicorn app.main:app
```

A API usa `http://127.0.0.1:8000` e a documentação interativa fica em `/docs`. Execute com um worker para manter o limite de chamadas ao Gemini e o balanceamento das atribuições no mesmo processo. O arquivo SQLite é criado automaticamente.

### Configuração

Defina `GEMINI_API_KEY` com uma chave do [Google AI Studio](https://aistudio.google.com/apikey) e `GEMINI_MODEL` com um ID de [modelo disponível](https://ai.google.dev/gemini-api/docs/models) que aceite os parâmetros do experimento. Com a chave ou o modelo em branco, apenas ELIZA participa de novas sessões. O SDK inicia de forma preguiçosa, na primeira chamada Gemini. As falhas do provedor retornam mensagens genéricas e o turno pode ser reenviado na mesma condição. `GEMINI_REQUESTS_PER_MINUTE` limita as tentativas por janela móvel de 60 segundos. Configure também `ADMIN_API_KEY` para habilitar os endpoints administrativos e `CORS_ORIGINS` como lista de origens separadas por vírgulas. Mantenha o arquivo `.env` no backend.

## Endpoints

Prefixo comum `/api/v1`.

| Método | Caminho | Uso |
|---|---|---|
| GET | `/health` | Aviso, disponibilidade e limites antes de iniciar |
| POST | `/experiments` | Inicia com `{"acknowledged": true}` |
| POST | `/experiments/{id}/messages` | Envia `{"content": "How was your day?"}` |
| GET | `/experiments/{id}/messages` | Consulta histórico e estado |
| POST | `/experiments/{id}/finish` | Encerra a conversa |
| POST | `/experiments/{id}/evaluation` | Registra avaliação definitiva |
| GET | `/experiments/{id}/reveal` | Revela o agente após a avaliação |
| GET | `/admin/results` | Consulta métricas por grupo |
| GET | `/admin/results/export` | Baixa CSV |
| GET | `/admin/prompts` | Consulta versões e hashes dos prompts |

Use `X-Admin-API-Key` nos três endpoints administrativos. A sequência de estados é `CREATED → IN_PROGRESS → AWAITING_EVALUATION → EVALUATED → REVEALED`. `CREATED` é o estado interno inicial. O POST de criação já retorna a sessão iniciada. Uma transição inválida retorna HTTP 409 e uma entrada inválida retorna 422.

Exemplo de avaliação:

```json
{
  "classification": "human",
  "confidence": 85,
  "naturalness": 4,
  "coherence": 5,
  "emotional_understanding": 3,
  "comment": "The responses felt spontaneous."
}
```

## Testes

Dentro de `backend/`, execute `..\venv\Scripts\python.exe -m pytest -q` no Windows ou `../venv/bin/python -m pytest -q` no Linux. Os testes são independentes da chave e usam dados sintéticos.
