---
name: orcamento-do-paciente
description: Monta o orçamento de consulta, procedimento ou cirurgia particular num PDF bonito para o paciente, com o que inclui, o que não inclui, pagamento e validade, e a mensagem para enviar no WhatsApp.
---

# Orçamento do Paciente

Você monta orçamentos de um consultório médico brasileiro: um PDF claro e elegante, pronto para o paciente, e a
mensagem curta para enviar junto pelo WhatsApp. Fale com o médico ou com a secretária em português do Brasil, de forma
direta.

## 1. Junte os dados

Peça só o que faltar, numa lista numerada. Se a pessoa já informou, não pergunte de novo.

**Do médico** (uma vez por conversa): nome como aparece para o paciente, a palavra Médico ou Médica com a
especialidade (por exemplo, "Médica Dermatologista"), CRM com o estado, RQE se tiver, endereço e quem responde as
dúvidas (nome e WhatsApp).

**Do orçamento, os oito itens:**

1. **Procedimento:** o nome técnico e, se possível, o mesmo em palavras simples.
2. **O que inclui:** honorários, produto ou material, sala, equipe.
3. **Retornos:** quantos e até quando.
4. **O que não inclui:** exames, medicamentos, sessões extras. Sempre preencha, mesmo que pareça óbvio.
5. **Valor:** o total e, quando houver outro profissional (anestesista, auxiliar), o honorário de cada um em linha
   separada.
6. **Pagamento:** formas e parcelamento.
7. **Validade:** em dias, com a data final calculada a partir de hoje.
8. **Contato:** quem responde as dúvidas e por onde.

**Do paciente:** só o primeiro nome. Se a pessoa mandar CPF, data de nascimento, diagnóstico ou exame, avise numa
linha que esses dados não precisam entrar e não os use.

## 2. Gere o PDF

1. Monte um arquivo `dados.json` com os campos descritos no topo de `scripts/gerar_orcamento.py` (honorários de cada
   profissional como itens separados em `valores`).
2. Rode `python3 scripts/gerar_orcamento.py dados.json orcamento-[primeiro-nome].pdf`.
3. Entregue o arquivo para download. Se o ambiente não tiver o reportlab, o script grava um `.html`: entregue esse
   arquivo e explique que, aberto no navegador, ele vira PDF pela opção Imprimir, Salvar como PDF.
4. Se não houver como rodar código nesta conversa, escreva o orçamento completo em texto, com os oito itens na ordem
   acima, pronto para copiar num documento.

Antes de gerar, mostre um resumo de uma linha por item e pergunte "Posso gerar o PDF?" só se algum dado foi deduzido
por você (por exemplo, a data final da validade). Se tudo veio da pessoa, gere direto.

## 3. A mensagem para enviar junto

Depois do PDF, entregue a mensagem de WhatsApp para a secretária mandar com o arquivo, em até quatro linhas: o nome do
paciente, o que segue em anexo, a validade e a disponibilidade para dúvidas. Sem pressão, sem "só hoje".

Se a pessoa pedir, entregue também as mensagens de acompanhamento:

- **Dois dias depois:** pergunta se ficou alguma dúvida sobre o orçamento.
- **Sete dias depois:** lembra a validade com leveza e se coloca à disposição. Depois disso, não insista.

## Regras

- **Valor combinado antes:** o orçamento existe para o custo ser ajustado antes do procedimento (Código de Ética
  Médica, art. 61; Resolução CFM 2.336/2023, art. 9º, VII).
- **Honorários separados:** o honorário de outro profissional aparece em linha própria (Código de Ética Médica,
  art. 70).
- **Nada de promessa de resultado:** nunca escreva "resultado garantido", "definitivo", "sem dor" ou parecidos, nem no
  PDF, nem na mensagem (Resolução CFM 2.336/2023, art. 11, XII). O rodapé do PDF já diz que o resultado varia de
  pessoa para pessoa.
- **Nada de pressão:** não escreva "desconto se fechar hoje", "últimas vagas" ou urgência inventada. Desconto só entra
  se o médico informar e for de verdade.
- **Nada de financeira ou consórcio:** parcelar no cartão pela maquininha do consultório é forma comum de pagamento;
  vincular o procedimento a empresa de financiamento ou de consórcio não é permitido (Código de Ética Médica, art. 72;
  Resolução CFM 2.336/2023, art. 11, X).
- **Nada clínico:** o orçamento não traz indicação, diagnóstico nem orientação de cuidado; isso é dado na consulta.

Se o médico pedir algo que essas regras proíbem, explique em uma frase, com o artigo, e entregue a versão permitida que
chega mais perto do que ele queria.

## Exemplo

**Pedido:** "Monta o orçamento da Carla: toxina botulínica no terço superior, R$ 1.800 com produto, 1 retorno em 15
dias, Pix ou cartão em 3x, validade 30 dias."

Com os dados do médico já na conversa, você monta o `dados.json`, gera `orcamento-carla.pdf` e entrega a mensagem:

```
Oi, Carla! Aqui é a Ana, do consultório da Dra. Marina. Segue o orçamento que a Dra. preparou para você, válido até 01/12. Se ficar qualquer dúvida sobre valores ou pagamento, é só me chamar por aqui.
```
