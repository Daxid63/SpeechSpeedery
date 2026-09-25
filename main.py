import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import time
import random

duration = 3  # 3 segundos costumam ser suficientes para uma única palavra
sample_rate = 44100
filename = "output.wav"

print('Bem vindo ao SpeechSpeedery!')
time.sleep(1)
print('Aqui você deve falar as palavras que aparecerem na tela, e o programa verifica se você falou corretamente.')
time.sleep(1)
print('Lembre que as palavras estarão em inglês, então você deve falar em inglês também.')
time.sleep(1)
print('Vamos começar!\n')

# Dicionário movido para fora do loop (boa prática)
dictionary = {
    'fácil': ['cat', 'dog', 'house', 'car', 'tree', 'book', 'sun', 'moon', 'star', 'water'],
    'médio': ['computer', 'bicycle', 'mountain', 'river', 'ocean', 'elephant', 'giraffe', 'umbrella', 'chocolate', 'piano'],
    'difícil': ['philosophy', 'psychology', 'architecture', 'astronomy', 'neurology', 'metamorphosis', 'photosynthesis', 'onomatopoeia']
}

# Inicializa a variável para permitir a entrada no loop
difficulty = ""

while difficulty not in ['fácil', 'médio', 'difícil']:
    difficulty = input('Selecione o nível de dificuldade (fácil, médio, difícil): ').strip().lower()
    
    if difficulty == 'fácil':
        print('Você selecionou o nível fácil. As palavras serão simples.\n')
    elif difficulty == 'médio':
        print('Você selecionou o nível médio. As palavras serão um pouco mais complexas.\n')
    elif difficulty == 'difícil':
        print('Você selecionou o nível difícil. As palavras serão bastante complexas.\n')
    else:
        print('Nível de dificuldade inválido. Por favor, tente novamente.')

# Sorteia uma palavra do nível escolhido para o desafio
target_word = random.choice(dictionary[difficulty])

print(f"Sua palavra é: {target_word.upper()}")
print("Gravando em 3... 2... 1... FALE!")

# Processo de gravação
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
sd.wait()
wav.write(filename, sample_rate, recording)
print("Gravação encerrada. Analisando...")

# Processo de reconhecimento de voz
recognizer = sr.Recognizer()
try:
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        # Define o idioma do recohecimento para inglês americano
        text_heard = recognizer.recognize_google(audio_data, language="en-US").lower()
        
        print(f"Eu entendi: \"{text_heard}\"")
        
        if text_heard == target_word:
            print("Parabéns! Você acertou a pronúncia!")
        else:
            print(f"Quase lá! A palavra correta era '{target_word}', mas parece que você disse '{text_heard}'.")
            
except sr.UnknownValueError:
    print("Não consegui entender o áudio. Tente falar mais claro ou ajuste o volume do microfone.")
except sr.RequestError:
    print("Erro de conexão com o serviço de reconhecimento de voz.")