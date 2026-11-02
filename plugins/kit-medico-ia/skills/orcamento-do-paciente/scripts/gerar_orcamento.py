#!/usr/bin/env python3
"""Gera o PDF do orçamento do paciente a partir de um arquivo JSON. Versão 1.1, revisada em 02/11/2026.

Uso:
  python3 gerar_orcamento.py --conferir dados.json      confere os dados e mostra o resumo dos oito itens, sem gerar
  python3 gerar_orcamento.py dados.json orcamento-[procedimento]-[aaaa-mm-dd].pdf
Se o reportlab não estiver instalado, grava um HTML no lugar (mesmo nome, extensão .html), que abre no navegador e
pode ser salvo em PDF pela impressão.

Campos do JSON (todos obrigatórios, salvo os marcados como opcionais):
  medico: {nome, titulo (com a palavra Médico ou Médica), crm (com o estado), rqe (opcional), endereco (opcional)}
  data: data de emissão, "02/11/2026"
  Os oito itens:
  1 procedimento: nome técnico            procedimento_simples (opcional): o mesmo em palavras simples
  2 inclui: ["item", ...]
  3 retornos: texto, ou "não se aplica" (só quando o médico autorizou)
  4 nao_inclui: ["item", ...]
  5 valores: [{"item": "...", "valor": ...}, ...] um item por profissional; valor maior que zero, em número (1800 ou
    1800.5) ou em texto brasileiro ("1.800,00", "R$ 1.800,00", "1800,50"); no máximo dois dígitos de centavos
  6 pagamento: ["forma", ...] (se escrever "3x de R$ 600,00", a conta precisa fechar com o total)
  7 validade: texto com a data final, "15 dias, até 17/11/2026" (dias corridos a partir da data de emissão)
  8 contato: quem responde as dúvidas e por onde, ou "não se aplica" (só quando o médico autorizou)
  observacoes (opcional): texto            cor (opcional): "#0E5E6F"

O PDF não leva nome nem dado do paciente: sai com a linha "Paciente:" em branco, para a clínica preencher fora da IA.
Nenhum campo pode ter marcador entre colchetes, como [valor]: documento com pendência não vira PDF.
"""
import datetime, html, json, math, re, sys, unicodedata
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

CENTAVO = Decimal('0.01')
PROIBIDAS = {  # frase: motivo
    'resultado garantido': 'promessa de resultado (Resolução CFM 2.336/2023, art. 11, XII)',
    'garantia de resultado': 'promessa de resultado (Resolução CFM 2.336/2023, art. 11, XII)',
    'resultado definitivo': 'promessa de resultado (Resolução CFM 2.336/2023, art. 11, XII)',
    'sem dor': 'insinua resultado e esconde complicação (Resolução CFM 2.336/2023, art. 11, XII)',
    'se fechar hoje': 'pressão para fechar; desconto só real, sem urgência inventada',
    'so hoje': 'pressão para fechar; desconto só real, sem urgência inventada',
    'ultimas vagas': 'pressão para fechar; desconto só real, sem urgência inventada',
    'consorcio': 'venda por consórcio é proibida (Resolução CFM 2.336/2023, art. 11, X)',
}


class Erro(Exception):
    pass


def sem_acento(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn').lower()


def nao_se_aplica(t):
    return re.sub(r'[^a-z ]', '', sem_acento(t)).strip() == 'nao se aplica'


def numero(v):
    """Valor em reais como Decimal. Aceita 1800, 1800.5, "1800", "1.800", "1.800,00", "R$ 1.800,00" e "1800,50"."""
    if isinstance(v, bool) or v is None or isinstance(v, (list, dict)):
        raise Erro('precisa ser um número, como 1800, ou um texto como "1.800,00"')
    if isinstance(v, (int, float)):
        if isinstance(v, float) and not math.isfinite(v):
            raise Erro('não é um número de verdade (NaN ou infinito)')
        d = Decimal(str(v))
    else:
        t = str(v).replace('R$', '').replace(' ', '').replace(' ', '').strip()
        if not t:
            raise Erro('está vazio')
        if not re.fullmatch(r'-?[0-9.,]+', t):
            raise Erro('"%s" não é um valor em reais; use só números, como 1800 ou "1.800,00"' % v)
        if ',' in t:
            t = t.replace('.', '').replace(',', '.')
        elif t.count('.') > 1 or (t.count('.') == 1 and len(t.split('.')[1]) == 3):
            t = t.replace('.', '')   # 1.800 = mil e oitocentos
        try:
            d = Decimal(t)
        except InvalidOperation:
            raise Erro('"%s" não é um valor em reais; use só números, como 1800 ou "1.800,00"' % v)
    if not d.is_finite():
        raise Erro('não é um número de verdade (NaN ou infinito)')
    if d.as_tuple().exponent < -2:
        raise Erro('tem mais de dois dígitos de centavos')
    if d <= 0:
        raise Erro('precisa ser maior que zero (valor negativo ou zero não entra no orçamento)')
    return d.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def reais(d):
    s = '{:,.2f}'.format(d).replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + s


def data_br(t):
    m = re.fullmatch(r'(\d{2})/(\d{2})/(\d{4})', t.strip())
    if not m:
        raise Erro('use o formato dd/mm/aaaa, como 02/11/2026')
    try:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        raise Erro('"%s" não é uma data que existe' % t)


def conferir(d):
    """Confere tudo e devolve os dados prontos. Junta todos os problemas antes de parar."""
    erros = []

    def texto(chave, valor, rotulo):
        if not isinstance(valor, str) or not valor.strip():
            erros.append('%s: falta preencher (precisa ser um texto).' % rotulo)
            return None
        return valor.strip()

    def lista(chave, rotulo):
        v = d.get(chave)
        if not isinstance(v, list) or not v:
            erros.append('%s: precisa ser uma lista com pelo menos um item, como ["Honorários médicos"].' % rotulo)
            return None
        if not all(isinstance(i, str) and i.strip() for i in v):
            erros.append('%s: cada item da lista precisa ser um texto preenchido.' % rotulo)
            return None
        return [i.strip() for i in v]

    if not isinstance(d, dict):
        raise Erro('O arquivo precisa ser um objeto JSON, entre chaves { }, com os campos do orçamento.')

    if 'paciente' in d:
        erros.append('paciente: o PDF não leva o nome nem dados do paciente. Tire o campo "paciente" do JSON; se a '
                     'clínica quiser o nome no documento, ela escreve depois, fora da IA.')

    m = d.get('medico')
    if not isinstance(m, dict):
        erros.append('medico: falta o bloco do médico, com nome, titulo e crm.')
        m = {}
    nome = texto('nome', m.get('nome'), 'medico.nome')
    titulo = texto('titulo', m.get('titulo'), 'medico.titulo')
    crm = texto('crm', m.get('crm'), 'medico.crm')
    if titulo and 'medic' not in sem_acento(titulo):
        erros.append('medico.titulo: precisa ter a palavra Médico ou Médica, como "Médica Dermatologista" '
                     '(Resolução CFM 2.336/2023, art. 4º, I).')
    if crm and 'crm' not in crm.lower():
        erros.append('medico.crm: escreva com a sigla e o estado, como "CRM-CE 12345".')
    for opc in ('rqe', 'endereco'):
        if opc in m and (not isinstance(m[opc], str) or not m[opc].strip()):
            erros.append('medico.%s: se vier, precisa ser um texto preenchido.' % opc)

    emissao = None
    if isinstance(d.get('data'), str):
        try:
            emissao = data_br(d['data'])
        except Erro as e:
            erros.append('data: %s.' % e)
    else:
        erros.append('data: falta a data de emissão, como "02/11/2026".')

    procedimento = texto('procedimento', d.get('procedimento'), '1. procedimento')
    if 'procedimento_simples' in d:
        texto('procedimento_simples', d.get('procedimento_simples'), 'procedimento_simples')
    inclui = lista('inclui', '2. inclui (o que está incluso)')
    retornos = texto('retornos', d.get('retornos'), '3. retornos (escreva quantos e até quando, ou "não se aplica" '
                     'se o médico autorizou)')
    nao_inclui = lista('nao_inclui', '4. nao_inclui (o que não está incluso)')

    total = None
    valores = d.get('valores')
    if not isinstance(valores, list) or not valores:
        erros.append('5. valores: precisa ser uma lista de itens, como [{"item": "Honorários médicos", "valor": 1800}].')
    else:
        soma, ok = Decimal('0'), True
        for i, v in enumerate(valores, 1):
            if not isinstance(v, dict) or not isinstance(v.get('item'), str) or not v.get('item', '').strip():
                erros.append('5. valores, linha %d: precisa ter "item" (texto) e "valor".' % i)
                ok = False
                continue
            if 'valor' not in v:
                erros.append('5. valores, linha %d (%s): falta o valor.' % (i, v['item']))
                ok = False
                continue
            try:
                v['valor_decimal'] = numero(v['valor'])
                soma += v['valor_decimal']
            except Erro as e:
                erros.append('5. valores, linha %d (%s): o valor %s.' % (i, v['item'], e))
                ok = False
        if ok:
            total = soma.quantize(CENTAVO, rounding=ROUND_HALF_UP)

    pagamento = lista('pagamento', '6. pagamento (formas e parcelamento)')
    if pagamento and total is not None:
        for p in pagamento:
            for vezes, parcela in re.findall(r'(\d{1,2})\s*x\s*de\s*(?:R\$\s*)?([0-9][0-9.,]*)', p, flags=re.I):
                try:
                    pv = numero(parcela.rstrip('.,'))
                except Erro:
                    erros.append('6. pagamento: não entendi o valor da parcela em "%s".' % p)
                    continue
                n = int(vezes)
                if n < 1 or abs(pv * n - total) > CENTAVO * n:
                    erros.append('6. pagamento: "%s" dá %s, e o total é %s. Corrija a parcela ou o total.'
                                 % (p, reais(pv * n), reais(total)))

    validade = texto('validade', d.get('validade'), '7. validade')
    if validade and emissao:
        datas = re.findall(r'\d{2}/\d{2}/\d{4}', validade)
        if not datas:
            erros.append('7. validade: escreva também a data final, como "15 dias, até 17/11/2026".')
        else:
            try:
                fim = data_br(datas[-1])
                if fim < emissao:
                    erros.append('7. validade: a data final (%s) é anterior à data de emissão (%s).'
                                 % (datas[-1], d['data']))
                dias = re.search(r'(\d+)\s*dias', validade)
                if dias and fim != emissao + datetime.timedelta(days=int(dias.group(1))):
                    certo = (emissao + datetime.timedelta(days=int(dias.group(1)))).strftime('%d/%m/%Y')
                    erros.append('7. validade: %s dias corridos a partir de %s terminam em %s, e o texto diz %s.'
                                 % (dias.group(1), d['data'], certo, datas[-1]))
            except Erro as e:
                erros.append('7. validade: %s.' % e)

    contato = d.get('contato', m.get('contato'))
    contato = texto('contato', contato, '8. contato (quem responde as dúvidas e por onde, ou "não se aplica" se o '
                    'médico autorizou)')

    if 'observacoes' in d:
        texto('observacoes', d.get('observacoes'), 'observacoes')
    if 'cor' in d and not (isinstance(d['cor'], str) and re.fullmatch(r'#[0-9A-Fa-f]{6}', d['cor'])):
        erros.append('cor: use uma cor no formato "#0E5E6F".')

    # Marcadores e frases proibidas em qualquer texto
    def textos(o, caminho):
        if isinstance(o, str):
            yield caminho, o
        elif isinstance(o, dict):
            for k, v in o.items():
                if k != 'valor_decimal':
                    yield from textos(v, (caminho + '.' if caminho else '') + k)
        elif isinstance(o, list):
            for i, v in enumerate(o, 1):
                yield from textos(v, '%s[%d]' % (caminho, i))
    for caminho, t in textos(d, ''):
        if re.search(r'\[[^\]]*\]', t):
            erros.append('%s: ainda tem marcador entre colchetes ("%s"). Preencha antes de gerar.' % (caminho, t))
        for frase, motivo in PROIBIDAS.items():
            if re.search(r'\b%s\b' % frase, sem_acento(t)):
                erros.append('%s: tire "%s": %s.' % (caminho, frase, motivo))

    if erros:
        raise Erro('O orçamento não foi gerado. Corrija estes pontos e rode de novo:\n- ' + '\n- '.join(erros))

    d['total'] = total
    d['contato'] = contato
    d.setdefault('cor', '#0E5E6F')
    return d


def carregar(caminho):
    try:
        texto = Path(caminho).read_text(encoding='utf-8')
    except OSError:
        raise Erro('Não achei o arquivo %s.' % caminho)

    def constante(c):
        raise Erro('O arquivo tem o valor %s, que não é um número de verdade. Use um valor em reais, como 1800.' % c)
    try:
        d = json.loads(texto, parse_constant=constante)
    except json.JSONDecodeError as e:
        raise Erro('O arquivo não é um JSON válido (linha %d, coluna %d): confira vírgulas, aspas e chaves.'
                   % (e.lineno, e.colno))
    return conferir(d)


def resumo(d):
    def r(t):
        return 'Não se aplica.' if nao_se_aplica(t) else t
    linhas = ['Resumo para conferir antes do PDF (data de emissão %s):' % d['data'],
              '1. Procedimento: %s' % d['procedimento'],
              '2. Inclui: %s' % '; '.join(d['inclui']),
              '3. Retornos: %s' % r(d['retornos']),
              '4. Não inclui: %s' % '; '.join(d['nao_inclui']),
              '5. Valor: %s · Total %s' % ('; '.join('%s %s' % (v['item'], reais(v['valor_decimal']))
                                                     for v in d['valores']), reais(d['total'])),
              '6. Pagamento: %s' % '; '.join(d['pagamento']),
              '7. Validade: %s' % d['validade'],
              '8. Contato: %s' % r(d['contato'])]
    return '\n'.join(linhas)


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

    def talvez(t):
        return 'Não se aplica a este orçamento.' if nao_se_aplica(t) else t

    ident = '%s · %s' % (e(m['titulo']), e(m['crm'])) + (' · %s' % e(m['rqe']) if m.get('rqe') else '')
    cab = Table([[Paragraph(e(m['nome']), est['nome'])], [Paragraph(ident, est['cab'])]]
                + ([[Paragraph(e(m['endereco']), est['cab'])]] if m.get('endereco') else []),
                colWidths=[largura])
    cab.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), cor), ('LEFTPADDING', (0, 0), (-1, -1), 7 * mm),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 7 * mm), ('TOPPADDING', (0, 0), (0, 0), 6 * mm),
                             ('BOTTOMPADDING', (0, -1), (-1, -1), 6 * mm)]))

    proc = e(d['procedimento']) + (' <font color="#5A7680">(%s)</font>' % e(d['procedimento_simples'])
                                   if d.get('procedimento_simples') else '')
    linhas = [[Paragraph(e(v['item']), est['txt']), Paragraph(reais(v['valor_decimal']), est['valor'])]
              for v in d['valores']]
    linhas.append([Paragraph('Total', est['total']), Paragraph(reais(d['total']), est['totalv'])])
    valores = Table(linhas, colWidths=[largura * 0.68, largura * 0.32])
    valores.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -2), 0.6, linha), ('LINEABOVE', (0, -1), (-1, -1), 1.2, cor),
                                 ('BACKGROUND', (0, -1), (-1, -1), fundo), ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2.2 * mm),
                                 ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2 * mm), ('LEFTPADDING', (0, 0), (-1, -1), 3 * mm),
                                 ('RIGHTPADDING', (0, 0), (-1, -1), 3 * mm)]))

    corpo = [cab, Spacer(1, 8 * mm), Paragraph('Orçamento', est['titulo']),
             Paragraph('Data: %s &nbsp;&nbsp;·&nbsp;&nbsp; Paciente: ______________________________' % e(d['data']),
                       est['txt'])]
    corpo += secao('Procedimento', [Paragraph(proc, est['txt'])])
    corpo += secao('O que está incluso', lista(d['inclui']))
    corpo += secao('Retornos', [Paragraph(e(talvez(d['retornos'])), est['txt'])])
    corpo += secao('O que não está incluso', lista(d['nao_inclui']))
    corpo += secao('Valor', [valores])
    corpo += secao('Formas de pagamento', lista(d['pagamento']))
    corpo += secao('Validade', [Paragraph(e(d['validade']), est['txt'])])
    corpo += secao('Dúvidas', [Paragraph(e(talvez(d['contato'])), est['txt'])])
    if d.get('observacoes'):
        corpo += secao('Observações', [Paragraph(e(d['observacoes']), est['txt'])])
    corpo += [Spacer(1, 8 * mm), Paragraph(
        'Valor combinado antes da realização do procedimento. O resultado varia de pessoa para pessoa, e as orientações '
        'de cuidado são dadas na consulta.', est['nota'])]

    SimpleDocTemplate(str(saida), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title='Orçamento · %s · %s' % (d['procedimento'], d['data']),
                      author=m['nome'], subject='Orçamento', creator='Kit Médico IA').build(corpo)
    return saida


def gerar_html(d, saida):
    e = lambda t: html.escape(str(t))
    talvez = lambda t: 'Não se aplica a este orçamento.' if nao_se_aplica(t) else t
    m, cor = d['medico'], d['cor']
    li = lambda itens: '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(i) for i in itens)
    sec = lambda r, c: '<h3>%s</h3>%s' % (r, c)
    ident = ' · '.join(e(x) for x in (m['titulo'], m['crm'], m.get('rqe')) if x)
    linhas = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (e(v['item']), reais(v['valor_decimal'])) for v in d['valores'])
    partes = [sec('Procedimento', '<p>%s%s</p>' % (e(d['procedimento']), ' (%s)' % e(d['procedimento_simples'])
                                                     if d.get('procedimento_simples') else '')),
              sec('O que está incluso', li(d['inclui'])),
              sec('Retornos', '<p>%s</p>' % e(talvez(d['retornos']))),
              sec('O que não está incluso', li(d['nao_inclui'])),
              sec('Valor', '<table>%s<tr class="t"><td>Total</td><td>%s</td></tr></table>' % (linhas, reais(d['total']))),
              sec('Formas de pagamento', li(d['pagamento'])),
              sec('Validade', '<p>%s</p>' % e(d['validade'])),
              sec('Dúvidas', '<p>%s</p>' % e(talvez(d['contato']))),
              sec('Observações', '<p>%s</p>' % e(d['observacoes'])) if d.get('observacoes') else '']
    doc = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Orçamento · %s · %s</title><style>
body{font-family:Helvetica,Arial,sans-serif;color:#16323C;max-width:720px;margin:24px auto;padding:0 20px}
header{background:%s;color:#fff;padding:24px 28px;border-radius:10px}header b{font-size:22px}
h1{color:%s}h3{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5A7680;margin:22px 0 6px}
table{width:100%%;border-collapse:collapse}td{padding:8px;border-bottom:1px solid #D5E7E8}td+td{text-align:right}
tr.t td{font-weight:bold;color:%s;background:#F3F9F9;border-top:2px solid %s}small{color:#5A7680}
</style></head><body><header><b>%s</b><br>%s%s</header><h1>Orçamento</h1>
<p>Data: %s · Paciente: ______________________________</p>%s<p><small>Valor combinado antes da realização do
procedimento. O resultado varia de pessoa para pessoa, e as orientações de cuidado são dadas na consulta.</small></p>
</body></html>''' % (e(d['procedimento']), e(d['data']), cor, cor, cor, cor, e(m['nome']), ident,
                     '<br>' + e(m['endereco']) if m.get('endereco') else '', e(d['data']), ''.join(partes))
    saida = Path(saida).with_suffix('.html')
    saida.write_text(doc, encoding='utf-8')
    return saida


def main(args):
    if len(args) == 2 and args[0] == '--conferir':
        print(resumo(carregar(args[1])))
        return
    if len(args) != 2:
        sys.exit(__doc__)
    dados = carregar(args[0])
    try:
        import reportlab  # noqa: F401
        print(gerar_pdf(dados, args[1]))
    except ImportError:
        print(gerar_html(dados, args[1]))


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Erro as e:
        print(e, file=sys.stderr)
        sys.exit(1)
