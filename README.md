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
   **Privacidade**, desligue **Help improve our AI models**.
2. Baixe o ZIP da skill (na aula do módulo ou na tabela acima), sem abrir.
3. Em **Personalização > Skills**, clique em **+ Adicionar > Fazer upload de Skill**, escolha o ZIP e clique em
   **Fazer upload**.
4. Em **Skills > Meus**, confira se a skill está na lista com a chave ligada.

### Rota 2 · caminho por ZIP no ChatGPT

1. Em **Configurações > Controles de dados**, desligue **Melhorar o modelo para todo mundo**.
2. Baixe o ZIP da skill, sem abrir.
3. Em **Plugins > Habilidades**, clique em **Adicionar > Carregar do seu computador** e escolha o ZIP.
4. Confira se a skill aparece em **Instaladas**.

### Rota 3 · pacote por marketplace no Claude (plano pago, as quatro de uma vez)

Este repositório funciona como um **marketplace** (o catálogo) com um **plugin** (o pacote das quatro skills).

1. Em **Personalização > Plugins**, clique em **+ Adicionar > Adicionar marketplace > Adicionar de um repositório**.
2. Cole `https://github.com/samuelbatista04/kit-medico-ia` no campo **URL** e clique na opção
   **Usar "https://github.com/samuelbatista04/kit-medico-ia"**, logo embaixo.
3. Deixe ligada a chave **Sincronizar automaticamente** e clique em **Sincronizar**.
4. Na aba **Descobrir**, procure **kit-medico-ia** e clique em **Adicionar**.

O mesmo pacote chega ao Claude Code da mesma conta (versão 2.1.273 ou mais nova).

### Rota 4 · instalação no Codex (fica só naquele computador)

No Codex (app do ChatGPT para computador, Codex CLI ou extensão de editor), numa conversa nova, peça ao Skill
Installer com o endereço completo da pasta da skill:

```
$skill-installer instale a skill desta pasta do GitHub: https://github.com/samuelbatista04/kit-medico-ia/tree/main/plugins/kit-medico-ia/skills/anuncio-do-medico
```

Para as quatro de uma vez:

```
$skill-installer instale do repositório samuelbatista04/kit-medico-ia as pastas plugins/kit-medico-ia/skills/anuncio-do-medico, plugins/kit-medico-ia/skills/secretaria-do-consultorio, plugins/kit-medico-ia/skills/orcamento-do-paciente e plugins/kit-medico-ia/skills/conteudo-do-medico
```

Aprove o acesso à internet se o Codex pedir. Confira digitando `$` e procurando a skill; se não aparecer, feche e abra o
Codex. A skill instalada assim não aparece no site chatgpt.com.

### Rota 5 · instalação no Claude Code (plano pago, fica só naquele computador)

Digite um comando de cada vez:

```
/plugin marketplace add samuelbatista04/kit-medico-ia
```

```
/plugin install kit-medico-ia@kit-medico-ia
```

Escolha **Install for you (user scope)**. Se o resumo pedir, digite `/reload-plugins`. Confira digitando `/` e
procurando `/kit-medico-ia:anuncio-do-medico`.

## Teste de instalação

1. Confira que a skill aparece ligada na lista do app (Rotas 1 e 3: Skills > Meus e a lista do `/`; Rota 2:
   Instaladas; Rota 4: lista do `$`; Rota 5: lista do `/`).
2. Numa conversa nova, cole o pedido de teste (dados fictícios, sem CRM e sem RQE de propósito):

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
| Rota 1 (ZIP no Claude) | Não | Baixe o ZIP novo, exclua a antiga (Skills > Meus, abra, desligue a chave, **...** > Excluir) e envie o novo |
| Rota 2 (ZIP no ChatGPT) | Não | Baixe o ZIP novo, remova a antiga em Instaladas (menu **...**) e carregue o novo |
| Rota 3 (marketplace) | A tela do Claude promete manter o plugin atualizado com Sincronizar automaticamente ligada | A primeira atualização vai mostrar como conferir |
| Rota 4 (Codex) | Não | O instalador não substitui pasta existente: mova a pasta antiga para a Lixeira (em geral, `~/.codex/skills/anuncio-do-medico`) e repita o pedido |
| Rota 5 (Claude Code) | Não, até você ligar | Em `/plugin` > Marketplaces > kit-medico-ia > Enable auto-update, ou rode `claude plugin update kit-medico-ia@kit-medico-ia`. `claude plugin list` mostra a versão |

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
