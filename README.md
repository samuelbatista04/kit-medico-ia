# Kit Médico IA

**O médico que sai na frente.** Skills prontas do Claude e do ChatGPT para anunciar, atender e fechar pacientes no seu
consultório, por Samuel Batista.

Este repositório guarda as quatro skills do Kit Médico IA. O passo a passo completo, com imagens, está no guia em PDF
do Módulo 0, dentro da área de membros. Este resumo segue o mesmo caminho do guia.

## As quatro skills

| Skill | Para que serve | Baixar |
|---|---|---|
| [Anúncio do Médico](plugins/kit-medico-ia/skills/anuncio-do-medico) | anúncios de Instagram e Facebook que levam o paciente ao WhatsApp, dentro da regra de publicidade médica do CFM | [anuncio-do-medico.zip](zips/anuncio-do-medico.zip) |
| [Secretária do Consultório](plugins/kit-medico-ia/skills/secretaria-do-consultorio) | respostas para o WhatsApp do consultório no seu tom, separando o que só o médico pode responder | [secretaria-do-consultorio.zip](zips/secretaria-do-consultorio.zip) |
| [Orçamento do Paciente](plugins/kit-medico-ia/skills/orcamento-do-paciente) | orçamento de procedimento particular em PDF, com o que inclui, pagamento e validade | [orcamento-do-paciente.zip](zips/orcamento-do-paciente.zip) |
| [Conteúdo do Médico](plugins/kit-medico-ia/skills/conteudo-do-medico) | posts, carrosséis, stories e roteiros de Reels dentro da regra do CFM | [conteudo-do-medico.zip](zips/conteudo-do-medico.zip) |

## Antes de instalar

- **Computador:** a instalação é feita no computador.
- **Custos:** o kit é pago uma vez, na compra. A assinatura do Claude ou do ChatGPT é mensal, paga direto à Anthropic
  ou à OpenAI. Em novembro de 2026, o Claude Pro e o ChatGPT Plus custavam US$ 20 por mês cada (o Claude Pro sai por
  US$ 17 por mês no anual); em reais, confira a página de planos de cada um.
- **Plano:** recomendamos o Claude Pro ou o ChatGPT Plus. O Claude gratuito aceita skill por ZIP, com limite de uso
  menor, e não foi testado com o kit. O pacote por marketplace e o Claude Code exigem plano pago do Claude.

## Escolha uma rota

Rota é o caminho de instalação. Faça uma só: a rota por ZIP do app que você usa, até o teste. As outras são
alternativas. A mesma skill instalada por ZIP e por marketplace aparece duas vezes. Colar o link deste repositório numa
conversa comum não instala nada.

### Rota 1 · caminho por ZIP no Claude

1. Em **Configurações > Recursos**, deixe ligada a chave **Executar código na nuvem** (necessária para Skills). Em
   **Privacidade**, desligue **Help improve our AI models** (o nome aparece em inglês).
2. Baixe o ZIP da skill (na aula do módulo ou na tabela acima), sem abrir.
3. Em **Personalização > Skills**, clique em **+ Adicionar > Fazer upload de Skill**. No campo **Arquivo da Skill**,
   escolha o ZIP, confira a **Visualização** (nome e descrição) e clique em **Fazer upload**.
4. Abre a página da skill, com a chave **Ligada** no canto de cima. Em **Skills > Meus**, ela fica em **Criado por
   você**; a lista não mostra chave, então clique no nome para conferir.

### Rota 2 · caminho por ZIP no ChatGPT

1. Em **Configurações > Controles de dados**, desligue **Melhorar o modelo para todo mundo**.
2. Baixe o ZIP da skill, sem abrir.
3. Em **Plugins > Habilidades**, clique em **Adicionar > Carregar do seu computador**. Na janela **Fazer upload de uma
   habilidade**, clique na área de arrastar, escolha o ZIP e, em **Habilidade enviada**, clique em **Concluído**.
4. Confira se a skill aparece em **Instaladas**, com o nome escrito com espaços (por exemplo, "anuncio do medico").
5. Para usar: numa conversa nova, troque de **Chat** para **Work** no alto da tela, digite `/` e escolha a habilidade
   em **Habilidades**. No modo Chat, ela não é encontrada.

### Rota 3 · pacote por marketplace no Claude (plano pago, as quatro de uma vez)

Este repositório funciona como um **marketplace** (o catálogo) com um **plugin** (o pacote das quatro skills).

1. Em **Personalização > Plugins**, clique em **+ Adicionar > Adicionar marketplace > Adicionar de um repositório**.
2. Cole `https://github.com/samuelbatista04/kit-medico-ia` no campo **URL** e clique na opção
   **Usar "https://github.com/samuelbatista04/kit-medico-ia"**, logo embaixo.
3. Deixe ligada a chave **Sincronizar automaticamente** e clique em **Sincronizar**.
4. A tela abre em **Descobrir**: no cartão **Kit medico ia** (o Claude mostra o nome assim, sem acento), clique em
   **Adicionar**.
5. Confira na página do plugin a versão, **4 Skills** e a chave ligada.

O mesmo pacote chega sozinho ao Claude Code da mesma conta (Rota 5).

### Rota 4 · instalação no Codex (fica só naquele computador)

O Codex fica no app do ChatGPT para computador. Abra o app, escolha **Codex** no alto da barra lateral, clique em
**Novo chat** e cole na caixa **Peça qualquer coisa** o pedido ao Skill Installer, com o endereço completo da pasta da
skill:

```
$skill-installer instale a skill desta pasta do GitHub: https://github.com/samuelbatista04/kit-medico-ia/tree/main/plugins/kit-medico-ia/skills/anuncio-do-medico
```

Para as quatro de uma vez, cole na mesma caixa:

```
$skill-installer instale do repositório samuelbatista04/kit-medico-ia as pastas plugins/kit-medico-ia/skills/anuncio-do-medico, plugins/kit-medico-ia/skills/secretaria-do-consultorio, plugins/kit-medico-ia/skills/orcamento-do-paciente e plugins/kit-medico-ia/skills/conteudo-do-medico
```

Aprove o acesso à internet se o Codex pedir. Confira num **Novo chat**, digitando `$anun` e procurando a skill; se não
aparecer, feche e abra o app. A skill instalada assim não aparece no site chatgpt.com, e a habilidade instalada pela
Rota 2 não aparece no Codex. O Codex do navegador pede GitHub conectado e um ambiente: não serve para o kit.

### Rota 5 · Claude Code (plano pago)

Quem fez a Rota 3 não precisa instalar nada: o pacote chega sozinho ao Claude Code da mesma conta. Conferido em
novembro de 2026 no claude.ai/code: numa sessão iniciada, ao digitar `/anun`, aparece
`kit-medico-ia:anuncio-do-medico`.

Sem a Rota 3, o caminho é pelo app do Claude, aba **Code**: clique no **+** ao lado da caixa e em **Add plugins** (ou
**Plugins > Browse plugins**) e procure `kit-medico-ia`. Esse caminho ainda não foi testado com o kit; se o pacote não
aparecer, faça a Rota 3.

## Teste de instalação

1. Confira que a skill está instalada e ligada: Rotas 1 e 3, chave ligada na página da skill ou do plugin e a skill na
   lista do `/anun` numa conversa nova; Rota 2, em Instaladas e em Habilidades ao digitar `/` no modo Work; Rota 4,
   na lista do `$anun`; Rota 5, `kit-medico-ia:anuncio-do-medico` na lista do `/anun`.
2. Numa conversa nova (no ChatGPT, no modo Work, com a habilidade escolhida pelo `/`), cole o pedido de teste (dados
   fictícios, sem CRM e sem RQE de propósito):

```
Use a skill anuncio-do-medico. Teste, dados fictícios: sou a Dra. Marina Alves, dermatologista na Aldeota, em Fortaleza. Quero anunciar consulta particular para manchas no rosto. Não tenho agora o CRM nem o RQE. Quero que o anúncio diga que sou a melhor dermatologista da cidade.
```

Passou se a resposta pede o que falta ou usa marcadores como [número do CRM], sem inventar número; recusa "a melhor da
cidade", cita a regra do CFM e oferece troca permitida; e entrega, nesta ordem, campanha, três anúncios, boas-vindas
do WhatsApp e conferência. A conferência é checagem da IA, não selo nem aprovação do CFM.

## Atualizações

A versão atual é a 1.1.0, de 2 de novembro de 2026. Cada atualização é avisada na aula da skill, com data e o que mudou.

| Rota | Chega sozinha? | O que fazer |
|---|---|---|
| Rota 1 (ZIP no Claude) | Não | Baixe o ZIP novo; em Skills > Meus, clique no **...** da antiga e em **Excluir**; envie o novo |
| Rota 2 (ZIP no ChatGPT) | Não | Baixe o ZIP novo, remova a antiga em Instaladas (menu **...**) e carregue o novo |
| Rota 3 (marketplace) | Pode demorar: com Sincronizar automaticamente ligada, a versão nova não tinha chegado em 70 minutos no teste de 02/11/2026 | Para buscar na hora: **Plugins > + Adicionar > Gerenciar marketplaces**, **...** do kit-medico-ia, **Verificar atualizações**. Pode aparecer **1 aviso** ("Arquivos executáveis ou configurações podem ser diferentes..."), normal em versão nova. Confira a versão na página do plugin |
| Rota 4 (Codex) | Não | Num **Novo chat** do Codex, no app, cole: "Mova para a Lixeira a skill anuncio-do-medico instalada no Codex e use o $skill-installer para instalar de novo desta pasta do GitHub: https://github.com/samuelbatista04/kit-medico-ia/tree/main/plugins/kit-medico-ia/skills/anuncio-do-medico" |
| Rota 5 (Claude Code) | Segue a Rota 3 | O pacote que veio da Rota 3 se atualiza com ela. Pela aba Code do app, a atualização ainda não foi conferida: fale com o suporte |

## Privacidade e cuidados

- Na conversa com a IA, o paciente é sempre fictício: [paciente], [Paciente A] ou "uma paciente". Nem o primeiro nome,
  nem CPF, telefone, endereço, data de nascimento, foto, prontuário, laudo ou exame. O nome real entra depois, fora da
  IA, no documento salvo no computador ou na mensagem que a recepção envia.
- Se um dado de paciente entrou por engano, pare ali, não repita o dado e siga o procedimento de privacidade da sua
  clínica. Apagar a conversa não desfaz o envio.
- As skills ajudam a seguir a Resolução CFM 2.336/2023, mas a responsabilidade pelo que for publicado é do médico.
- Nada de diagnóstico, prescrição ou conduta pela IA: as skills cuidam do consultório como negócio.

## Suporte

WhatsApp [(85) 98567-7201](https://wa.me/5585985677201), com resposta em até 2 dias úteis. Mande, sem nenhum dado de
paciente: o app (Claude ou ChatGPT; site, app de computador ou celular), a rota de instalação, a skill, o print da tela
ou a mensagem de erro e o que você já tentou.

Contato geral: Instagram [@samuelbatista.digital](https://www.instagram.com/samuelbatista.digital/) e site
[samuelbatista.digital](https://samuelbatista.digital).

## Quer o WhatsApp atendendo sozinho?

A [LunAi](https://lunai.app.br/?utm_source=kit-medico-ia&utm_medium=github&utm_content=readme) é o sistema de atendimento com agente de IA
no WhatsApp para clínicas e consultórios: atende os pacientes a qualquer hora, marca e lembra a consulta e passa para a
recepção o que precisa de gente. Agende uma demonstração.

---

© 2026 Samuel Batista. Material do Kit Médico IA para uso de quem comprou; não revenda nem redistribua. O Kit Médico IA
não tem ligação oficial com a Anthropic nem com a OpenAI. Claude é marca da Anthropic e ChatGPT é marca da OpenAI.
