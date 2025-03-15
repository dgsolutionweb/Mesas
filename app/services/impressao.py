from app.models.models import ConfiguracaoSistema, ItemComanda
import win32print
import win32con
from datetime import datetime

class ServicoImpressao:
    @staticmethod
    def imprimir_pedido(item_comanda):
        config = ConfiguracaoSistema.query.first()
        if not config:
            return False

        # Determina se é um item para cozinha ou bar
        categorias_cozinha = config.categorias_cozinha.split(',')
        categorias_bar = config.categorias_bar.split(',')
        
        if item_comanda.produto.categoria in categorias_cozinha and config.imprimir_pedidos_cozinha:
            impressora = config.impressora_cozinha
            imprimir = True
        elif item_comanda.produto.categoria in categorias_bar and config.imprimir_pedidos_bar:
            impressora = config.impressora_bar
            imprimir = True
        else:
            imprimir = False

        if not imprimir or not impressora:
            return False

        try:
            # Prepara o conteúdo da impressão
            conteudo = []
            conteudo.append('=' * 40)
            conteudo.append(f'{config.nome_restaurante}'.center(40))
            conteudo.append('=' * 40)
            conteudo.append(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
            conteudo.append(f'Mesa: {item_comanda.comanda.mesa.numero}')
            conteudo.append(f'Comanda: {item_comanda.comanda.id}')
            conteudo.append('-' * 40)
            conteudo.append('NOVO PEDIDO')
            conteudo.append('-' * 40)
            conteudo.append(f'Item: {item_comanda.produto.nome}')
            conteudo.append(f'Quantidade: {item_comanda.quantidade}')
            if item_comanda.observacao:
                conteudo.append(f'Obs: {item_comanda.observacao}')
            conteudo.append('-' * 40)
            if config.mensagem_rodape:
                conteudo.append(config.mensagem_rodape.center(40))
                conteudo.append('-' * 40)
            conteudo.append('\n' * 3)  # Espaço para corte
            
            # Junta todo o conteúdo
            texto_final = '\n'.join(conteudo)
            
            # Configura a impressora
            hprinter = win32print.OpenPrinter(impressora)
            try:
                hJob = win32print.StartDocPrinter(hprinter, 1, ("Pedido", None, "RAW"))
                try:
                    win32print.StartPagePrinter(hprinter)
                    win32print.WritePrinter(hprinter, texto_final.encode('utf-8'))
                    win32print.EndPagePrinter(hprinter)
                finally:
                    win32print.EndDocPrinter(hprinter)
            finally:
                win32print.ClosePrinter(hprinter)
            
            return True
        except Exception as e:
            print(f"Erro ao imprimir: {str(e)}")
            return False 