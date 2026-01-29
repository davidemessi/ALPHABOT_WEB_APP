import RPi.GPIO as GPIO   # Libreria per controllare i pin GPIO del Raspberry Pi
import time               # Libreria per le funzioni di temporizzazione

# Definizione della classe AlphaBot per controllare il robot
class AlphaBot(object):
	
	def __init__(self,in1=12,in2=13,ena=6,in3=20,in4=21,enb=26):
		# Assegnazione dei pin a variabili interne
		self.IN1 = in1   # Pin direzione motore destro
		self.IN2 = in2   # Pin direzione motore destro
		self.IN3 = in3   # Pin direzione motore sinistro
		self.IN4 = in4   # Pin direzione motore sinistro
		self.ENA = ena   # Pin PWM motore destro
		self.ENB = enb   # Pin PWM motore sinistro

		# Configurazione GPIO
		GPIO.setmode(GPIO.BCM)      # Usa numerazione BCM dei pin (non quella fisica)
		GPIO.setwarnings(False)     # Disabilita gli avvisi
		GPIO.setup(self.IN1,GPIO.OUT)   # Imposta pin IN1 come uscita
		GPIO.setup(self.IN2,GPIO.OUT)   # Imposta pin IN2 come uscita
		GPIO.setup(self.IN3,GPIO.OUT)   # Imposta pin IN3 come uscita
		GPIO.setup(self.IN4,GPIO.OUT)   # Imposta pin IN4 come uscita
		GPIO.setup(self.ENA,GPIO.OUT)   # Imposta pin ENA (PWM destro) come uscita
		GPIO.setup(self.ENB,GPIO.OUT)   # Imposta pin ENB (PWM sinistro) come uscita
		
		self.forward()   # Imposta inizialmente i motori in avanti

		# Configurazione PWM (controllo velocità) a 500 Hz
		self.PWMA = GPIO.PWM(self.ENA,500)  
		self.PWMB = GPIO.PWM(self.ENB,500)

		# Avvio del PWM con duty cycle al 50% (velocità media)
		self.PWMA.start(50)   
		self.PWMB.start(50)

	# Funzione per andare avanti
	def forward(self):
		GPIO.output(self.IN1,GPIO.HIGH)  # Motore destro avanti
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)   # Motore sinistro avanti
		GPIO.output(self.IN4,GPIO.HIGH)

	# Funzione per fermare i motori
	def stop(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)

	# Funzione per andare indietro
	def backward(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.HIGH)
		GPIO.output(self.IN3,GPIO.HIGH)
		GPIO.output(self.IN4,GPIO.LOW)

	# Funzione per girare a sinistra
	def left(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)

	# Funzione per girare a destra
	def right(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)
		
	# Imposta velocità del motore destro
	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)   # Cambia duty cycle PWM

	# Imposta velocità del motore sinistro
	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)	
		
	# Imposta velocità e direzione di entrambi i motori
	def setMotor(self, left, right):
		# Controllo motore destro
		if((right >= 0) and (right <= 100)):  # Valori positivi = avanti
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)): # Valori negativi = indietro
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)

		# Controllo motore sinistro
		if((left >= 0) and (left <= 100)):   # Avanti
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)): # Indietro
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)
