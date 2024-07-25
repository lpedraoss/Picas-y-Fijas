import random
import itertools

class SmartAgentPick:
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
        self.posibles_numeros = list(itertools.permutations('0123456789', 4))

    def generar_numero_aleatorio(self):
        while True:
            numero = ''.join(random.sample('0123456789', 4))
            if numero not in self.numeros_intentados:
                self.numeros_intentados.add(numero)
                return numero

    def adivinar_numero(self):
        if self.intentos == 0:
            numero_secreto = self.generar_numero_aleatorio()
        else:
            numero_secreto = self.posibles_numeros[0]
        self.intentos += 1
        print("Intento {}: {}".format(self.intentos, ''.join(numero_secreto)))
        self.ultimo_intento = numero_secreto
        return ''.join(numero_secreto)

    def verificar_picas_fijas(self, intento, picas, fijas):
        nuevas_posibles = []
        for numero in self.posibles_numeros:
            picas_count = sum((1 for i, digit in enumerate(numero) if digit in intento and intento[i] != digit))
            fijas_count = sum((1 for i, digit in enumerate(numero) if intento[i] == digit))
            if picas_count == picas and fijas_count == fijas:
                nuevas_posibles.append(numero)
        self.posibles_numeros = nuevas_posibles

    def actualizar_resultados(self, picas, fijas):
        self.verificar_picas_fijas(self.ultimo_intento, picas, fijas)
        
    def adivinar_recursivo(self, picas, fijas):
        if self.ultimo_intento is None:
            intento_agente = self.adivinar_numero()
        else:
            self.actualizar_resultados(picas, fijas)
            if self.posibles_numeros:
                intento_agente = ''.join(self.posibles_numeros[0])
            else:
                intento_agente = self.generar_numero_aleatorio()
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
agente = SmartAgentPick()
print("Piensa en un número de 4 dígitos.")
input("Cuando estés listo, presiona Enter para que el agente comience a adivinar...")
# Primer intento del agente
primer_intento = agente.adivinar_numero()
# Solicitar picas y fijas del primer intento
picas = int(input("Picas del primer intento: "))
fijas = int(input("Fijas del primer intento: "))
# Continuar adivinando
agente.adivinar_recursivo(picas, fijas)

