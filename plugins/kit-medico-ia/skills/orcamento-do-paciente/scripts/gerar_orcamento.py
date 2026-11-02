#!/usr/bin/env python3
"""Gera o PDF do orçamento do paciente a partir de um arquivo JSON.

Uso: python3 gerar_orcamento.py dados.json orcamento.pdf
Se o reportlab não estiver instalado, grava um HTML no lugar (mesmo nome, extensão .html), que abre no navegador e
pode ser salvo em PDF pela impressão.

Campos do JSON (os marcados com * são obrigatórios):
  medico*: {nome*, titulo*, crm*, rqe, endereco, contato}
  paciente*: primeiro nome            data*: "01/11/2026"
  procedimento*: nome técnico         procedimento_simples: o mesmo em palavras simples
  inclui*: [itens]                    retornos: texto
  nao_inclui*: [itens]                valores*: [{item, valor}] (honorários de cada profissional separados;
                                      valor em número, 1800, ou no formato brasileiro, "1.800,00")
  pagamento*: [formas]                validade*: texto
  observacoes: texto                  cor: "#0E5E6F"
"""
import html, json, sys
from pathlib import Path


def numero(v):
    """Aceita 1800, 1800.5, "1800", "1.800,00", "R$ 1.800,00" e "1800,50"."""
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).replace('R$', '').replace(' ', '').strip()
    if ',' in t:
        t = t.replace('.', '').replace(',', '.')
    elif t.count('.') > 1 or (t.count('.') == 1 and len(t.split('.')[1]) == 3):
        t = t.replace('.', '')   # 1.800 = mil e oitocentos
    return float(t)


def reais(v):
    s = '{:,.2f}'.format(numero(v)).replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + s


def carregar(caminho):
    d = json.loads(Path(caminho).read_text(encoding='utf-8'))
    faltam = [c for c in ('medico', 'paciente', 'data', 'procedimento', 'inclui', 'nao_inclui', 'valores',
                          'pagamento', 'validade') if not d.get(c)]
    faltam += ['medico.' + c for c in ('nome', 'titulo', 'crm') if not d.get('medico', {}).get(c)]
    if faltam:
        sys.exit('Faltam campos: ' + ', '.join(faltam))
    try:
        d['total'] = sum(numero(v['valor']) for v in d['valores'])
    except (KeyError, ValueError):
        sys.exit('Valor inválido em "valores": use número, como 1800, ou "1.800,00".')
    d.setdefault('cor', '#0E5E6F')
    return d


def gerar_pdf(d, saida):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    cor = colors.HexColor(d['cor'])
    texto = colors.HexColor('#16323C')
    suave = colors.HexColor('#5A7680')
    linha = colors.HexColor('#D5E7E8')
    fundo = colors.HexColor('#F3F9F9')
    m = d['medico']
    e = lambda t: html.escape(str(t))

    est = {
        'nome': ParagraphStyle('nome', fontName='Helvetica-Bold', fontSize=16, leading=19, textColor=colors.white),
        'cab': ParagraphStyle('cab', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.white),
        'titulo': ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=cor,
                                 spaceAfter=2 * mm),
        'rot': ParagraphStyle('rot', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=suave),
        'txt': ParagraphStyle('txt', fontName='Helvetica', fontSize=10.5, leading=15, textColor=texto),
        'forte': ParagraphStyle('forte', fontName='Helvetica-Bold', fontSize=10.5, leading=15, textColor=texto),
        'total': ParagraphStyle('total', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=cor),
        'valor': ParagraphStyle('valor', fontName='Helvetica-Bold', fontSize=10.5, leading=15, textColor=texto,
                                alignment=2),
        'totalv': ParagraphStyle('totalv', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=cor, alignment=2),
        'nota': ParagraphStyle('nota', fontName='Helvetica', fontSize=8.5, leading=12, textColor=suave),
    }
    largura = A4[0] - 36 * mm

    def secao(rotulo, conteudo):
        return [Spacer(1, 5 * mm), Paragraph(rotulo.upper(), est['rot']), Spacer(1, 1.5 * mm)] + conteudo

    def lista(itens):
        return [Paragraph('• ' + e(i), est['txt']) for i in itens]

    ident = '%s · %s' % (e(m['titulo']), e(m['crm'])) + (' · %s' % e(m['rqe']) if m.get('rqe') else '')
    cab = Table([[Paragraph(e(m['nome']), est['nome'])], [Paragraph(ident, est['cab'])]]
                + ([[Paragraph(e(m['endereco']), est['cab'])]] if m.get('endereco') else []),
                colWidths=[largura])
    cab.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), cor), ('LEFTPADDING', (0, 0), (-1, -1), 7 * mm),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 7 * mm), ('TOPPADDING', (0, 0), (0, 0), 6 * mm),
                             ('BOTTOMPADDING', (0, -1), (-1, -1), 6 * mm)]))

    proc = e(d['procedimento']) + (' <font color="#5A7680">(%s)</font>' % e(d['procedimento_simples'])
                                   if d.get('procedimento_simples') else '')
    linhas = [[Paragraph(e(v['item']), est['txt']), Paragraph(reais(v['valor']), est['valor'])] for v in d['valores']]
    linhas.append([Paragraph('Total', est['total']), Paragraph(reais(d['total']), est['totalv'])])
    valores = Table(linhas, colWidths=[largura * 0.68, largura * 0.32])
    valores.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -2), 0.6, linha), ('LINEABOVE', (0, -1), (-1, -1), 1.2, cor),
                                 ('BACKGROUND', (0, -1), (-1, -1), fundo), ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2.2 * mm),
                                 ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2 * mm), ('LEFTPADDING', (0, 0), (-1, -1), 3 * mm),
                                 ('RIGHTPADDING', (0, 0), (-1, -1), 3 * mm)]))

    corpo = [cab, Spacer(1, 8 * mm), Paragraph('Orçamento', est['titulo']),
             Paragraph('Paciente: <b>%s</b> &nbsp;&nbsp;·&nbsp;&nbsp; Data: %s' % (e(d['paciente']), e(d['data'])),
                       est['txt'])]
    corpo += secao('Procedimento', [Paragraph(proc, est['txt'])])
    corpo += secao('O que está incluso', lista(d['inclui']))
    if d.get('retornos'):
        corpo += secao('Retornos', [Paragraph(e(d['retornos']), est['txt'])])
    corpo += secao('O que não está incluso', lista(d['nao_inclui']))
    corpo += secao('Valor', [valores])
    corpo += secao('Formas de pagamento', lista(d['pagamento']))
    corpo += secao('Validade', [Paragraph(e(d['validade']), est['txt'])])
    if d.get('observacoes'):
        corpo += secao('Observações', [Paragraph(e(d['observacoes']), est['txt'])])
    if m.get('contato'):
        corpo += secao('Dúvidas', [Paragraph(e(m['contato']), est['txt'])])
    corpo += [Spacer(1, 8 * mm), Paragraph(
        'Valor combinado antes da realização do procedimento. O resultado varia de pessoa para pessoa, e as orientações '
        'de cuidado são dadas na consulta.', est['nota'])]

    SimpleDocTemplate(str(saida), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title='Orçamento · ' + d['paciente'], author=m['nome']).build(corpo)
    return saida


def gerar_html(d, saida):
    e = lambda t: html.escape(str(t))
    m, cor = d['medico'], d['cor']
    li = lambda itens: '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(i) for i in itens)
    sec = lambda r, c: '<h3>%s</h3>%s' % (r, c)
    ident = ' · '.join(e(x) for x in (m['titulo'], m['crm'], m.get('rqe')) if x)
    linhas = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (e(v['item']), reais(v['valor'])) for v in d['valores'])
    partes = [sec('Procedimento', '<p>%s%s</p>' % (e(d['procedimento']), ' (%s)' % e(d['procedimento_simples'])
                                                     if d.get('procedimento_simples') else '')),
              sec('O que está incluso', li(d['inclui'])),
              sec('Retornos', '<p>%s</p>' % e(d['retornos'])) if d.get('retornos') else '',
              sec('O que não está incluso', li(d['nao_inclui'])),
              sec('Valor', '<table>%s<tr class="t"><td>Total</td><td>%s</td></tr></table>' % (linhas, reais(d['total']))),
              sec('Formas de pagamento', li(d['pagamento'])),
              sec('Validade', '<p>%s</p>' % e(d['validade'])),
              sec('Observações', '<p>%s</p>' % e(d['observacoes'])) if d.get('observacoes') else '',
              sec('Dúvidas', '<p>%s</p>' % e(m['contato'])) if m.get('contato') else '']
    doc = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Orçamento</title><style>
body{font-family:Helvetica,Arial,sans-serif;color:#16323C;max-width:720px;margin:24px auto;padding:0 20px}
header{background:%s;color:#fff;padding:24px 28px;border-radius:10px}header b{font-size:22px}
h1{color:%s}h3{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5A7680;margin:22px 0 6px}
table{width:100%%;border-collapse:collapse}td{padding:8px;border-bottom:1px solid #D5E7E8}td+td{text-align:right}
tr.t td{font-weight:bold;color:%s;background:#F3F9F9;border-top:2px solid %s}small{color:#5A7680}
</style></head><body><header><b>%s</b><br>%s%s</header><h1>Orçamento</h1>
<p>Paciente: <b>%s</b> · Data: %s</p>%s<p><small>Valor combinado antes da realização do procedimento. O resultado varia
de pessoa para pessoa, e as orientações de cuidado são dadas na consulta.</small></p></body></html>''' % (
        cor, cor, cor, cor, e(m['nome']), ident, '<br>' + e(m['endereco']) if m.get('endereco') else '',
        e(d['paciente']), e(d['data']), ''.join(partes))
    saida = Path(saida).with_suffix('.html')
    saida.write_text(doc, encoding='utf-8')
    return saida


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    dados = carregar(sys.argv[1])
    try:
        import reportlab  # noqa: F401
        print(gerar_pdf(dados, sys.argv[2]))
    except ImportError:
        print(gerar_html(dados, sys.argv[2]))
