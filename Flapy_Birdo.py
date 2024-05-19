import pygame as pg
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/pipe.png"))
IMAGEM_CHAO = pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/Base.png"))
IMAGEM_FUNDO = pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/Bg.png"))
IMAGEMS_PASSARO = [
    pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/Bird1.png")),
    pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/Bird2.png")),
    pg.transform.scale2x(pg.image.load("Meu_primeiro_jogo.py/Bird3.png"))
    ]

pg.font.init()
FONTE_PONTOS = pg.font.SysFont("arialblack", 50)

class Passaro:
    IMGS = IMAGEMS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0 
        self.imagem = self.IMGS[0]
        
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
        
    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        
        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
    
        self.y += deslocamento
        
        # angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 30):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
                
    def desenhar(self, tela):
        # deeinir qual imagem o passaro vai usar
        self.contagem_imagem += 1
        
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
        
        # se o passaro tive caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2
            
        # desenhar a imagem
        imagem_rotacinada = pg.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft= (self.x, self.y)).center
        retangulo = imagem_rotacinada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacinada, retangulo.topleft)
        
    def get_mask(self):
        return pg.mask.from_surface(self.imagem)
 
 
class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5 
    
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pg.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()
        
    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA
        
    def mover(self):
        self.x -= self.VELOCIDADE
         
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))
    
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pg.mask.from_surface(self.CANO_TOPO)
        base_mask = pg.mask.from_surface(self.CANO_BASE)
        
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
    
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        
        if base_ponto or topo_ponto:
            return True
        else:
            return False
            
            
class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO
    
    def __init__(self, y):
        self. y = y
        self.x0 = 0
        self.x1 = self.LARGURA
        
    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE
        
        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA
    
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))
         
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_FUNDO, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
        
    texto = FONTE_PONTOS.render(f"{pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 15 - texto.get_width(), 0))
    chao.desenhar(tela)
    pg.display.update()
    
def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pg.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pg.time.Clock()
    
    rodando = True
    while rodando:
        relogio.tick(30)
        
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                rodando = False
                pg.quit()
                quit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
    
        for passaro in passaros:
            passaro.mover()
            
        chao.mover()
        
        adicionar_cano = False
        
        remover_canos = []
        
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
                
        if adicionar_cano:
            pontos += 1 
            canos.append(Cano(600))
        
        for cano in remover_canos:
            canos.remove(cano)
            
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                        
        desenhar_tela(tela, passaros, canos, chao, pontos)    

if __name__ == '__main__':       
    main()
