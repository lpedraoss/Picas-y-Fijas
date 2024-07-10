import random
import itertools

class AgentPick:
    """
    AgentPick
    ------------
    Agente Inteligente para picas y fijas
    Grupo: Sin grupo

    """
    def __init__(self):
        self.intentos = 0
        self.ultimo_intento = None
        self.numeros_intentados = set()
        self.resultados = {
            'fijas': [None] * 4,  # None indica que la posición aún no se ha determinado
            'picas': set()  # Set de dígitos que son picas
        }
        self.posiciones_picas = {digit: set(range(4)) for digit in '0123456789'}  # Posibles posiciones para cada dígito
        self.digitos_excluidos = set()

    def generar_numero_aleatorio(self):
        while True:
            numero = ''.join(random.sample([digit for digit in '0123456789' if digit not in self.digitos_excluidos], 4))
            if numero not in self.numeros_intentados:
                self.numeros_intentados.add(numero)
                return numero

    def adivinar_numero(self):
        numero_secreto = self.generar_numero_aleatorio()
        self.intentos += 1
        print("Intento {}: {}".format(self.intentos, numero_secreto))
        self.ultimo_intento = numero_secreto
        return numero_secreto

    def verificar_picas_fijas(self, picas, fijas):
        intento_lista = list(self.ultimo_intento)
        posibles_numeros = []

        # Probar con las fijas conocidas
        for i in range(4):
            if self.resultados['fijas'][i] is not None:
                intento_lista[i] = self.resultados['fijas'][i]

        # Generar posibles combinaciones para las posiciones restantes
        posiciones_restantes = [i for i in range(4) if self.resultados['fijas'][i] is None]
        posibles_digitos = [digit for digit in '0123456789' if digit not in intento_lista and digit not in self.digitos_excluidos]

        for combinacion in itertools.permutations(posibles_digitos, len(posiciones_restantes)):
            intento_copia = intento_lista[:]
            for i, pos in enumerate(posiciones_restantes):
                intento_copia[pos] = combinacion[i]
            posible_numero = ''.join(intento_copia)
            if posible_numero not in self.numeros_intentados:
                posibles_numeros.append(posible_numero)

        if posibles_numeros:
            intento_nuevo = posibles_numeros[0]
        else:
            intento_nuevo = self.generar_numero_aleatorio()

        self.numeros_intentados.add(intento_nuevo)
        return intento_nuevo

    def actualizar_resultados(self, intento, picas, fijas):
        if picas == 0 and fijas == 0:
            self.digitos_excluidos.update(intento)
        else:
            for i, digito in enumerate(intento):
                if self.resultados['fijas'][i] is None:
                    if fijas > 0 and digito not in self.resultados['fijas']:
                        self.resultados['fijas'][i] = digito
                        fijas -= 1
                    elif picas > 0 and digito not in self.resultados['picas']:
                        self.resultados['picas'].add(digito)
                        picas -= 1
                if digito in self.resultados['fijas'] or digito in self.resultados['picas']:
                    self.posiciones_picas[digito].discard(i)

    def adivinar_recursivo(self, picas, fijas):
        if self.ultimo_intento is None:
            intento_agente = self.adivinar_numero()
        else:
            self.actualizar_resultados(self.ultimo_intento, picas, fijas)
            intento_agente = self.verificar_picas_fijas(picas, fijas)
            self.intentos += 1
            print("Intento {}: {}".format(self.intentos, intento_agente))
            self.ultimo_intento = intento_agente

        continuar = input("¿El agente ha adivinado el número? (s/n): ")
        if continuar.lower() == 'n':
            picas = int(input("Picas: "))
            fijas = int(input("Fijas: "))
            self.adivinar_recursivo(picas, fijas)
        elif continuar.lower() == 's':
            print("¡El agente ha adivinado tu número en {} intentos!".format(self.intentos))
        else:
            print("Respuesta no válida. Por favor, responde 's' o 'n'.")
            self.adivinar_recursivo(picas, fijas)

# Uso del agente
agente = AgentPick()
print("Piensa en un número de 4 dígitos.")
input("Cuando estés listo, presiona Enter para que el agente comience a adivinar...")
# Primer intento del agente
primer_intento = agente.adivinar_numero()
# Solicitar picas y fijas del primer intento
picas = int(input("Picas del primer intento: "))
fijas = int(input("Fijas del primer intento: "))
# Continuar adivinando
agente.adivinar_recursivo(picas, fijas)

