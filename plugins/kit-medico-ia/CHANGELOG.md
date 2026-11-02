# Histórico de mudanças do plugin Kit Médico IA

## 1.1.0, 02/11/2026

Revisão das quatro skills a partir do relatório crítico de 01/11/2026.

- **Todas:** paciente sempre como [paciente] ou "uma paciente"; se o pedido trouxer nome, CPF ou dado que identifique,
  a skill não repete e avisa para parar, sem prometer que o aviso apaga o que foi enviado. Saída com dado obrigatório
  faltando sai como "Rascunho com pendências", com a lista do que falta no topo. Conferência com três estados
  (conferido pela IA, pendente de validação, confirmado pelo médico), sem OK por dedução e sem nada com cara de selo
  ou aprovação do CFM.
- **Anúncio do Médico:** exemplo sem dado inventado; decisão depois de uns 7 dias por consultas e custo por consulta,
  dentro do limite de gasto definido pelo médico; formato exato das peças (1080x1350 no feed, 1080x1920 em stories e
  vídeo) e como transformar o texto em arquivo; nenhuma frase garante aprovação da Meta; repertório do que a
  resolução libera.
- **Secretária do Consultório:** nunca diz que avisou a médica, agendou ou enviou; separa mensagem para o paciente de
  tarefa da recepção; prazo de retorno só o da ficha; horário só com vagas conferidas pela recepção; dado novo na
  conversa atualiza a ficha.
- **Orçamento do Paciente:** não deduz materiais, retornos, exclusões nem pagamento; resumo dos oito itens antes do PDF;
  PDF sem nome do paciente, nem no arquivo nem no metadado; o script recusa valor negativo, zero, NaN, Infinity,
  estrutura inválida, marcador residual, parcela que não fecha e validade com data errada, exige os oito itens
  (retorno e contato inclusive, ou "não se aplica" autorizado) e responde em português.
- **Conteúdo do Médico:** antes e depois pelas quatro etapas do Manual de Publicidade Médica do CFM (pelo menos quatro
  pacientes diferentes, evoluções satisfatórias e insatisfatórias, complicações; edição só de recorte, luz, nitidez e
  tarja; vídeo com no mínimo 2 segundos por quadro; autorização revogável; nenhuma vantagem pela imagem); palavras de
  alerta lidas no contexto; informação de saúde pendente até o médico confirmar; formato de cada peça; repertório do
  que a resolução libera.
- **Regras do CFM (`references/regras-cfm.md`, versão 1.1):** mesmo texto nas skills de anúncio e de conteúdo e no
  mestre da produção.

## 1.0.0, 01/11/2026

Primeira versão das quatro skills.
