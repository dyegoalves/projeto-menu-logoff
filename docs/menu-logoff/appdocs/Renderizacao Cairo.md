---
tags: [ui, cairo, renderizacao, grafica]
relacionado: [[Interface de Sessão]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Renderização Cairo

Desenha manualmente o fundo arredondado da janela com transparência e efeitos visuais.

## Como funciona

O método `_on_draw()` é conectado ao evento `draw` do widget e executa:

### 1. Configuração geométrica

```python
w, h = alloc.width, alloc.height
r = 22  # border radius
```

### 2. Desenho do caminho arredondado

Função `rounded_rect(ctx)` constrói retângulo com cantos circulares:

```python
ctx.arc(r,     r,     r, -math.pi, -math.pi / 2)  # canto superior esquerdo
ctx.arc(w - r, r,     r, -math.pi / 2, 0)         # canto superior direito
ctx.arc(w - r, h - r, r, 0, math.pi / 2)          # canto inferior direito
ctx.arc(r,     h - r, r, math.pi / 2, math.pi)    # canto inferior esquerdo
ctx.close_path()
```

### 3. Limpeza alpha (OPERATOR_CLEAR)

```python
cr.set_operator(cairo.OPERATOR_CLEAR)
cr.paint()
```
Limpa toda área para transparência total (requerido pelo compositor).

### 4. Preenchimento glassy

```python
cr.set_source_rgba(25/255, 25/255, 25/255, 0.85)  # 85% opaco
cr.fill_preserve()
```

### 5. Bordas e brilho

```python
# Borda externa fina
cr.set_source_rgba(1, 1, 1, 0.12)
cr.set_line_width(1.2)
cr.stroke_preserve()

# Brilho interno sutil
cr.set_source_rgba(255/255, 255/255, 255/255, 0.05)
cr.set_line_width(0.8)
cr.stroke()
```

## Arquivos principais

- `app/main.py` — Método `_on_draw()` (linhas 205-243)

## Integrações

- [[Interface de Sessão]] — Conecta `_on_draw` ao evento `draw`
- [[Estilização CSS]] — CSS complementa com cores e fontes

## Configuração

**Parâmetros visuais:**
```python
r = 22  # Raio dos cantos (border-radius)
alpha = 0.85  # Opacidade do fundo
```

**Pré-requisitos:**
- `set_app_paintable(True)` — Permite desenho customizado
- `screen.is_composited()` — Compositor ativo necessário
- `get_rgba_visual()` — Visual com canal alpha

## Observações importantes

- **ORDER MATTERS**: `OPERATOR_CLEAR` deve vir antes do paint, senão alpha falha
- **fill_preserve()**: Mantém caminho para stroke subsequente
- **Compositor**: Sem compositor (ex: X11 sem compositor), transparência falha
- **Performance**: Cairo é acelerado por hardware na maioria dos casos
- **Estilo macOS**: Visual "glassy" com camadas de alpha e bordas sutis
- **Fallback**: Se visual RGBA não existir, usa visual padrão (sem transparência)
