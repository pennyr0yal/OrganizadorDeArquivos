# ===================== BIBLIOTECAS
import tkinter as tk
from tkinter import filedialog
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import PyPDF2
import re
import shutil
# ===================== CAMINHOS
PASTA_TESTES = os.path.join(os.getcwd(),'Teste')
PASTA = os.path.join(PASTA_TESTES,'Mover_aqui')    # Pode ser modificado para a pasta onde os arquivos são salvos originalmente
PASTA_DESTINO = os.path.join(PASTA_TESTES,'Faturas Recebidas')

REFERENCIA_EMPRESA = 'Empresa'    # Texto que sinaliza no PDF o nome da empresa que queremos extrair
REFERENCIA_DATA = 'Data de Emissão'    # Texto que sinaliza no PDF a data que queremos extrair

# ===================== SCRIPT

def extrair_texto_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            if len(leitor.pages) > 0:
                texto = leitor.pages[0].extract_text()
                return texto or ''
    except Exception as e:
        print(f'[Erro ao ler o PDF] {caminho_pdf}. Log do erro: {e}')
    return ''

def extrair_empresa_e_data(texto):
    if not texto:
        print('[Aviso] Texto vazio ao tentar extrair dados.')
        return None, None
    
    empresa = None
    data = None
    linhas = texto.splitlines()

    # Localiza o nome da empresa
    for linha in linhas:
        if linha.startswith(REFERENCIA_EMPRESA):
            empresa = linha[len(REFERENCIA_EMPRESA):].lstrip(': ').strip()     # Remove o label e os possíveis ':' e espaços
            break
    # Se não encontrou pela label, usa a primeira linha como fallback
    if not empresa and linhas:
        empresa = linhas[0].strip()

    # Localiza a data
    padrao = rf'{re.escape(REFERENCIA_DATA)}[:\s]+(\d{{2}}/\d{{2}}/\d{{4}})'
    match_data = re.search(padrao, texto)
    if match_data:
        data = match_data.group(1).strip()

    if not empresa or not data:
        print(f'[Erro] Empresa ou data não extraídas corretamente.\n--- Texto extraído ---\n{texto[:500]}...\n')

    return empresa, data

def renomear_e_mover_arquivo(caminho_origem, empresa, data):
    try:
        # Limpa e formata a data
        dia, mes, ano = data.split('/')
        data_formatada = f'{ano}-{mes}-{dia}'

        # Limpa o nome da empresa
        empresa_limpa = re.sub(r'[^\w\s]', '', empresa)
        empresa_limpa = re.sub(r'\s+', '_', empresa_limpa)

        novo_nome = f'{empresa_limpa}_{data_formatada}.pdf'
        pasta_destino = os.path.join(PASTA_DESTINO, ano, mes)
        os.makedirs(pasta_destino, exist_ok=True)    # Checa se a pasta de destino existe e, caso não exista, cria a pasta
        novo_caminho = os.path.join(pasta_destino, novo_nome)

        # Renomeia e move o arquivo para a pasta de destino
        if os.path.exists(novo_caminho):
            base, extensao = os.path.splitext(novo_nome)

            # Lida com a existência de mais de um arquivo da mesma empresa na mesma data
            count = 1
            while os.path.exists(os.path.join(pasta_destino, f'{base}_{count}{extensao}')):
                count += 1
            novo_nome = f'{base}_{count}{extensao}'
            novo_caminho = os.path.join(pasta_destino, novo_nome)

        shutil.move(caminho_origem, novo_caminho)
        print(f'Arquivo movido para: {novo_caminho}')
        return novo_caminho
    except Exception as e:
        print(f'[Erro ao mover/renomear] {caminho_origem}. Log do erro: {e}')

class InvoiceHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            print(f'Novo arquivo PDF detectado: {event.src_path}')
            max_tentativas = 5
            for tentativa in range(max_tentativas):
                try:
                    texto = extrair_texto_pdf(event.src_path)
                    empresa, data = extrair_empresa_e_data(texto)
                    if empresa and data:
                        renomear_e_mover_arquivo(event.src_path, empresa, data)
                    else:
                        print('Erro: Não foi possível extrair empresa ou data do PDF.')
                    break
                except PermissionError:
                    print(f'Arquivo está em uso, tentando novamente ({tentativa + 1}/{max_tentativas})...')
                    time.sleep(1)
                except Exception as e:
                    print(f'Erro ao processar o arquivo: {e}')
                    break

if __name__ == '__main__':
    if not os.path.exists(PASTA):
        print(f'Pasta não existe: {PASTA}')
        exit()

    event_handler = InvoiceHandler()
    observer = Observer()
    observer.schedule(event_handler, path=PASTA, recursive=False)
    observer.start()

    print(f'\n\nMonitorando a pasta: {PASTA}...')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
