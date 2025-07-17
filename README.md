# Organizador de Arquivos PDF

O programa monitora automaticamente uma pasta por arquivos `.pdf` (no exemplo, faturas de empresas diversas). Ao detectar um novo arquivo, extrai informações como empresa emissora e data de emissão, renomeia o arquivo no formato <Empresa>_<AAAA-MM-DD>.pdf e o organiza em subpastas por ano e mês.

## Funcionalidades

- Monitora uma pasta continuamente enquanto o programa está ativo, utilizando a biblioteca watchdog.
- Extrai o texto de PDFs usando PyPDF2.
- Identifica a empresa e data da fatura a partir de prefixos configuráveis no código (no exemplo, a linha que contém "Empresa" e a linha que contém "Data de Emissão").
- Move e renomeia os arquivos automaticamente para subpastas organizadas por ano e mês.
- Trata erros comuns, como arquivos em uso e informações ausentes.

## Como usar

1. Execute o arquivo .bat na pasta principal. O programa instalará o venv, as bibliotecas necessárias e exibirá uma mensagem: "Monitorando pasta...".
2. Na pasta Teste, há 6 arquivos fictícios de 3 empresas diferentes. Mova eles para a pasta "Mover_aqui".
3. O programa automaticamente criará as pastas e distribuirá os documentos renomeados.

## Observações

- O script foi desenvolvido para fins de portfólio e pode ser adaptado para casos reais de processamento de documentos.
- Uma melhoria possível é permitir que o usuário selecione a pasta a ser monitorada no momento da execução.
- Em PDFs baseados em imagens (scans), a extração via PyPDF2 pode falhar; nesses casos, a utilização de OCR seria necessária.

# Autora
Desenvolvido por Natalia Junghans

📧 natbjunghans@gmail.com
