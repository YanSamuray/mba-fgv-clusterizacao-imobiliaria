# Projeto Final — Aprendizado Não Supervisionado

Segmentação do mercado imobiliário da Califórnia com técnicas de clusterização
(dataset California Housing). O notebook de entrega é **`projetofinal.ipynb`**. Ele cobre:

- exploração dos dados, pré-processamento e engenharia de features;
- PCA e quatro algoritmos de clusterização (K-Means, DBSCAN, Ward e GMM);
- validação, caracterização dos segmentos e estratégias de negócio.

| Arquivo | Conteúdo |
|---|---|
| `projetofinal.ipynb` | notebook de entrega, executado e com as saídas salvas |
| `Projeto Final - Aprendizado Não Supervisionado.ipynb` | template original da disciplina |
| `docs/` | enunciado do projeto |
| `archive/` | versão anterior do notebook (apenas preparação de dados) |
| `data/` | arquivos externos baixados pelo notebook e segmentação exportada (fora do controle de versão) |

## Ambiente

- Python 3.14, selecionado pelo arquivo `.python-version`.
- [uv](https://docs.astral.sh/uv/) para instalar e gerenciar as dependências.
- Bibliotecas de análise: pandas, NumPy, Matplotlib, Seaborn, scikit-learn, GeoPandas e openpyxl.
- Ferramentas de desenvolvimento: IPython kernel (`ipykernel`) e JupyterLab.

As dependências estão declaradas em `pyproject.toml`, e as versões resolvidas
estão registradas em `uv.lock`. Mantenha ambos no controle de versão.

## Preparação

Mantenha o projeto numa pasta de caminho curto (nesta máquina,
`C:\Users\admin\projects\projetofinal`) e abra o terminal nela:

```powershell
Set-Location "$env:USERPROFILE\projects\projetofinal"
```

Caminhos muito longos, como os de pastas sincronizadas pelo OneDrive, passam do limite
de 260 caracteres do Windows quando o suporte a caminhos longos está desativado. Isso
causa erros de arquivo não encontrado ao importar Matplotlib e Jupyter.
Veja a [documentação da Microsoft sobre limites de caminhos](https://learn.microsoft.com/windows/win32/fileio/maximum-file-path-limitation).

Depois, sincronize o ambiente:

```powershell
uv sync --locked
```

O comando cria ou sincroniza a `.venv`, incluindo as ferramentas de desenvolvimento.
O `uv` utiliza a versão de Python indicada em `.python-version` e pode baixá-la
caso ela ainda não esteja instalada. A primeira instalação requer internet.

Não é necessário ativar a `.venv` para usar os comandos `uv run` abaixo.

## Executar no VS Code

1. No terminal posicionado na pasta do projeto, abra o VS Code com `code .`.
2. Tenha as extensões **Python** (`ms-python.python`) e **Jupyter** (`ms-toolsai.jupyter`) instaladas.
3. Abra `projetofinal.ipynb`.
4. No canto superior direito, clique em **Select Kernel / Selecionar Kernel**,
   escolha **Python Environments / Ambientes Python** e selecione
   `.venv\Scripts\python.exe` deste projeto.
5. Execute as células em ordem ou use **Run All / Executar Tudo**.

Se o VS Code já tiver outro interpretador selecionado, use
**Python: Select Interpreter** na paleta de comandos e selecione a `.venv`.
A seleção do kernel do notebook também deve apontar para esse ambiente.

## Executar no navegador

```powershell
uv run --locked python -m jupyterlab
```

Abra o notebook na interface do JupyterLab e utilize o kernel **Python 3 (ipykernel)**.
Execute o comando a partir da pasta do projeto. A chamada `python -m jupyterlab` usa
diretamente o interpretador escolhido pelo `uv` nesse caminho.
Para encerrar o servidor, pressione `Ctrl+C` no terminal e confirme quando solicitado.

## Executar no Google Colab

1. Envie `projetofinal.ipynb` ao Google Drive e abra-o com o Colab.
2. Use **Runtime → Run all** (Ambiente de execução → Executar tudo). O Colab já traz as
   bibliotecas usadas, incluindo o GeoPandas. A execução completa leva alguns minutos.
3. Para a entrega, compartilhe o link com a opção "qualquer pessoa com o link".

## Dados

- **California Housing:** obtido com `sklearn.datasets.fetch_california_housing(as_frame=True)`.
  Se esse download falhar, o notebook reconstrói a mesma tabela a partir de uma cópia pública.
  Depois do primeiro download, o scikit-learn reutiliza o cache em `scikit_learn_data`, na pasta
  do usuário.
- **Arquivos externos**, baixados uma única vez para `data/`:
  - limites dos condados (US Census Bureau, via Plotly);
  - litoral do Natural Earth na escala 1:10 milhões;
  - as maiores cidades dos EUA (Plotly);
  - a versão do Kaggle do dataset, usada apenas para validar a distância até a costa.
- **Saída:** `data/segmentos_california.csv`, com o segmento de cada block group.

A primeira execução precisa de internet.

## Verificar e manter o ambiente

```powershell
uv run --locked python --version
uv pip check
uv run --locked python -c "import pandas, numpy, matplotlib, seaborn, sklearn, geopandas, openpyxl, ipykernel, jupyterlab; print('Ambiente OK')"
```

Para adicionar uma biblioteca de análise:

```powershell
uv add nome-do-pacote
```

Para adicionar uma ferramenta de desenvolvimento:

```powershell
uv add --dev nome-do-pacote
```

Use esses comandos para manter `pyproject.toml`, `uv.lock` e `.venv` sincronizados.
Se o notebook ainda exibir a mensagem de que falta `ipykernel`, execute
`uv sync --locked`, selecione novamente o kernel da `.venv` e reinicie-o.

Referência: [integração oficial do uv com Jupyter e VS Code](https://docs.astral.sh/uv/guides/integration/jupyter/).
