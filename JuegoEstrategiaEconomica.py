import json

class JuegoEstrategiaEconomica:
    def __init__(self, nombre_jugador):
        self.nombre_jugador = nombre_jugador
        self.turno = 1
        self.recursos = 100
        self.beneficio = 0
        self.costo = 0
        self.cargar_datos_juego()
    
    def cargar_datos_juego(self):
        with open('narrativas.json', encoding='utf-8') as f:
            self.narrativas = json.load(f)
        with open('eventos.json', encoding='utf-8') as f:
            self.eventos = json.load(f)
        with open('problemas.json', encoding='utf-8') as f:
            self.problemas = json.load(f)
    
    def mostrar_narrativa(self):
        print(self.narrativas[str(self.turno)])
        self.costo = 0
    
    def manejar_evento(self):
        evento = self.eventos.get(str(self.turno))
        if evento:
            print(f"Evento: {evento['descripcion']}")
            self.recursos += evento['cambio_recursos']
            self.costo += evento['cambio_costos']
    
    def resolver_problema(self):
        problema = self.problemas.get(str(self.turno))
        if problema:
            print(f"Problema: {problema['descripcion']}")
            solucion = input("Introduce tu solución: ")
            if solucion.strip() == problema['solucion'].strip():
                self.beneficio += problema['beneficio']
                print("¡Solución correcta!")
                if (self.turno % 2 == 1): self.turno += 1 
            else:
                self.costo += problema['penalizacion']
                print("Solución incorrecta.")
                if (self.turno % 2 == 0): self.turno += 1
    
    def calcular_beneficio(self):
        beneficio_neto = self.beneficio - self.costo
        if beneficio_neto < 0:
            excedente = abs(beneficio_neto)
            self.recursos -= excedente
            self.beneficio = 0
            print(f"Beneficio es menor que 0. Restando {excedente} de los recursos.")
        else:
            self.beneficio = beneficio_neto
        print(f"Resumen del Turno {self.turno}: Beneficio Neto: {self.beneficio}, Recursos: {self.recursos}")
        return self.beneficio
    
    def siguiente_turno(self):
        self.turno += 1
        if self.turno > len(self.narrativas):
            print("Fin del juego. Has llegado al final de la narrativa.")
            return False
        return True
    
    def jugar(self):
        print(f"¡Bienvenido {self.nombre_jugador} al Juego de Estrategia Económica!")
        while True:
            print("")
            self.mostrar_narrativa()
            self.manejar_evento()
            self.resolver_problema()
            self.calcular_beneficio()
            if self.recursos <= 0:
                print("Has perdido el juego. Tu empresa ha quebrado.")
                break
            if not self.siguiente_turno():
                break

if __name__ == "__main__":
    nombre_jugador = input("Introduce tu nombre: ")
    juego = JuegoEstrategiaEconomica(nombre_jugador)
    juego.jugar()
