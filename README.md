# CodeCats: The Bug Hunt

## 🐱 Sobre o Jogo
CodeCats: The Bug Hunt é um roguelike leve e divertido onde você controla um gatinho programador preso dentro de um computador corrompido. O herói felino, conhecido como **CodeCat**, precisa atravessar servidores infectados, ativar terminais e erradicar vilões digitais para restaurar a ordem do código.

Inspirado por jogos com movimentação em grade e visão top-down, o objetivo do jogador é explorar ambientes randômicos, escapar de bugs digitais e ativar terminais para avançar por três fases cada vez mais desafiadoras.

## História
Em um dia comum de compilação, CodeCat foi sugado para dentro de seu próprio notebook após um erro bizarro em um terminal corrompido. Agora, ele está preso no ciberespaço, onde bugs ganharam forma física e sabotam a lógica do sistema.

Para voltar ao mundo real, CodeCat precisa ativar os terminais espalhados em cada fase do sistema e derrotar os vilões digitais que patrulham os servidores.

## Vilões Digitais Implementados
- **StackRoach** – Barata digital com chips colados nas costas
- **OverflowFly** – Mosca voadora com asas cheias de logs

Outros vilões foram planejados como expansão futura (ex: Bugzilla, NullPointer, Trojanito, Bitworm...), mas não estão presentes neste protótipo inicial.

## ⚖ Controles
- `W`, `A`, `S`, `D`: mover o CodeCat na grade
- `E`: interagir com terminais

## Mecânicas
- 3 fases geradas proceduralmente
- Terminal em posição aleatória para ativação
- Bugs se movimentam com velocidade crescente por fase
- Ao completar 3 fases, o jogador vence o jogo

## Atualizações Futuras e Expansão
Este projeto foi inicialmente criado para fins educacionais e de entrega de um desafio técnico. No entanto, seu conceito modular e baseado em PgZero permite evoluir para algo mais completo utilizando recursos adicionais do **Pygame** e bibliotecas auxiliares.

### Possíveis melhorias futuras:
- **Spritesheets e animações detalhadas** por ação (idle, walk, hit)
- **Flip horizontal** de sprites para direção correta do movimento
- **Sistema de vidas e ataques**, com cooldown e efeitos visuais
- **Power-ups e upgrades temporários** (velocidade, invencibilidade, etc)
- **Inventário de depuração** ("debug tools") como arma contra bugs
- **Sistema de fases com tilesets diferentes** (ex: BIOS corrompida, setor de memória RAM, câmara de antivírus)
- **IA mais complexa para vilões**, com patrulhamento ou perseguição
- **Salvamento e sistema de conquistas** com contagem de bugs squishados
- **Cutscenes simples** entre fases com textos narrativos
- **Suporte a joystick ou controle**

Essas melhorias requerem maior liberdade no tamanho do código e podem utilizar bibliotecas do próprio Pygame ou ferramentas como:
- `pygame.sprite.Group`
- `pygame.mixer.Sound` para efeitos
- `pygame.transform.flip` para flip horizontal

## 📄 Estrutura de Pastas do Projeto
```
codecats_game/
├── images/
│   ├── codecat/              # sprites do herói
│   ├── stackroach/           # vilão StackRoach
│   ├── overflowfly/          # vilão OverflowFly
│   ├── tile_floor.png
│   ├── tile_wall.png
│   └── tile_terminal.png
├── music/
│   └── bg_music.ogg
├── sounds/                   # vazio por enquanto
├── main.py                   # arquivo principal do jogo
├── test.py                   # utilitário de testes
└── README.md
```

---

Desenvolvido com carinho usando **PgZero + Python 3**

**CodeCats** – uma ode felina à depuração digital.
