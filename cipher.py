from collections import Counter

ETW = "QWERTZUIOASDFGHJKPYXCVBNML" # German keyboard layout
rotors = [
    # enigma d
    "LPGSZMHAEOQKVXRFYBUTNICJDW",
    "SLVGBTFXJQOHEWIRZYAMKPCNDU",
    "CJGDPSHKTURAWZXFMYNQOBVLIE"
 ]
reflector = "IMETCGFRAYSQBZXWLHKDVUPOJN"
turnovers = ["Y", "E", "N"]
indices = [0, 0, 0]

def set_indices(a, b, c):
    indices[0] = a % 26
    indices[1] = b % 26
    indices[2] = c % 26

def move_rotors():
  second_move = rotors[0][indices[0]] == turnovers[0]
  third_move = rotors[1][indices[1]] == turnovers[1]
  indices[0] = (indices[0]+1)%26
  if second_move:  
    indices[1] = (indices[1]+1)%26
  if third_move: # Double stepping
    indices[2] = (indices[2]+1)%26
    indices[1] = (indices[1]+1)%26

def lookup(letter, rotor_ind):
    ind = (ord(letter) - ord('A') + indices[rotor_ind]) % 26
    return rotors[rotor_ind][ind]

def lookup_reverse(letter, rotor_ind):
    ind = rotors[rotor_ind].find(letter)
    return chr(ord('A') + (ind - indices[rotor_ind]) % 26)

def lookup_reflector(letter):
    return reflector[ord(letter)-ord('A')]
    
def encrypt(letter):
  # TODO: etw?
  l = lookup(letter, 0)
  l2 = lookup(l, 1)
  l3 = lookup(l2, 2)
  l4 = lookup_reflector(l3)
  l5 = lookup_reverse(l4, 2)
  l6 = lookup_reverse(l5, 1)
  l7 = lookup_reverse(l6, 0)
  return l7

def encrypt_message(message):
    result = ""
    for c in message:
        move_rotors()
        result += encrypt(c)
    return result
